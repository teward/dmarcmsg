# coding=utf-8

import email.utils
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

import dmarcmsg.util.content_disposition


def _construct_dmarc_message(msg, list_name, list_address, moderated=False, allow_posts=True):
    multipart = msg.is_multipart()
    msg_components = {'To': msg['To'], 'From': msg['From'], 'Subject': msg['Subject'],
                      'Message-ID': email.utils.make_msgid(), 'Date': msg['Date'], 'Payloads': []}

    # Deconstruct original message into components for component dict.
    # Iterate through all parts of the email message.
    for part in msg.walk():
        if not part.is_multipart():
            # If we hit a non-multipart piece, we need to do stuff with it.
            # First, extract MIMEType data.
            maintype, subtype = part.get_content_type().split('/', 1)
            # Next, get the Content-Disposition.
            cdisp = part.get("Content-Disposition")
            if cdisp and not part.is_multipart():
                # If we have a Content-Disposition and we're not in a multipart piece of the message...
                # ... create a dict for easier searching of the cdisp.
                cdisp_d = dmarcmsg.util.content_disposition.dict_from_string(cdisp)
                if 'attachment' or 'inline' in cdisp_d:
                    # And if we're an attachment of some sort...

                    # Sanitize the filename.
                    attachfname = cdisp_d['filename'].strip('"')
                    attachfname = attachfname.replace('\r', '')
                    attachfname = attachfname.replace('\n', '')

                    # Construct the MIMEBase message part for this MIMEType...
                    data = MIMEBase(maintype, subtype)
                    # ... and sets the Content-Type parameters to whatever they were in the original part...
                    for param in part.get_params():
                        if param not in data.get_params():
                            data.set_param(param[0], param[1])
                    # ... and sets the Content-Transfer-Encoding from the original part...
                    if 'Content-Transfer-Encoding' in part.keys():
                        data.add_header('Content-Transfer-Encoding', part['Content-Transfer-Encoding'])
                    # ... then sets the Payload for the part...
                    data.set_payload(part.get_payload())
                    # ... and finally add it into the Payloads section of the components,
                    # as a tuple so we can identify it's got a filename and is an attachment.
                    msg_components['Payloads'].append((data, attachfname))
            else:
                # If we're not an attachment, we're probably something else.
                if part.is_multipart():
                    # Skip if multipart part.
                    continue

                if maintype == "text":
                    # We might be text, either Plain or HTML, so we need to add that to the payloads
                    # ... by constructing the text message part...
                    data = MIMEText(part.get_payload(), _subtype=subtype)
                    # ... and then adding it to the Payloads.
                    msg_components['Payloads'].append(data)
                else:
                    # Any other MIMEType isn't to be handled and we just skip over that part
                    # TODO: Properly format other MIMEType payloads.
                    continue

    if not multipart:
        # If we're not making a multipart message, then only build a single-part message to send.
        if len(msg_components['Payloads']) != 1:
            # However, if we aren't a multipart message and try to include more than one payload,
            # that's illegal and something is horribly wrong. So error.
            raise TypeError("You cannot have a non-multipart message with multiple payloads.")

        # We should only have one 'payload' that comprises the entire contents of the message,
        # so we should structure the MIMEBase object for the message.
        mimepart = msg_components['Payloads'][0]
        # Get the content type for this part, though...
        maintype, subtype = mimepart.get_content_type().split('/', 1)
        # ...so we can properly create the proper MIMETyped base mail object.
        newmsg = MIMEBase(maintype, subtype)
        # And then subsequently set this new MIMEBase object's payload and charset.
        newmsg.set_payload(mimepart.get_payload(), charset=mimepart.get_charset())
    else:
        # Multipart messages have an outer 'multipart/alternative' MIME container we use.
        newmsg = MIMEMultipart('alternative')

        # Iterate over all individual payloads to add to the multipart msg as individual
        # parts and attach them to the new multipart message.
        for payload in msg_components['Payloads']:
            if type(payload) is not tuple:
                # We don't need to repeat the 'MIME-Version' header everywhere; standard email client's don't
                # after all.  So, just remove that header from the message payload/part.
                del payload['MIME-Version']

                # Then, because of our custom 'payloads' holder, any non-tuple payload types
                # are just standard MIME parts, just add them directly.
                newmsg.attach(payload)
            else:
                # Tupled payload values are attachments, so handle them as such...
                # ... by first adding the content type parameter with the filename for 'text' type attachments...
                if payload[0].get_content_type().split('/', 1)[0] == "text":
                    payload[0].set_param('name', payload[1])
                # ... then by adding the valid Content-Disposition header for the attachment.
                payload[0].add_header('Content-Disposition', 'attachment', filename=payload[1])
                # ... and like with standard parts, don't repeat the MIME-Version header.
                del payload[0]['MIME-Version']
                # And finally, attach this payload to the multipart message.
                newmsg.attach(payload[0])

    # Now set headers properly.  These headers are set the same no matter whether we're using a multipart mesage
    # or a single part message.
    newmsg['To'] = msg_components['To']  # Set the "To" field to be the original "To" address.
    if len(msg['From'].split('<')) > 1:  # Determine if 'From' is formatted a specific way.
        # If it has 'Thomas Ward <teward@foo.bar>' for example, we need to split out the name for the restructuring.
        newmsg.add_header('From', "'{}' via '{}' <{}>".format(msg['From'].split('<')[0].strip(),
                                                              'Example List', 'list@example.com'))
    else:
        # Otherwise, we just use the email address.
        newmsg.add_header('From', "'{}' via '{}' <{}>".format(msg['From'], 'Example List', 'list@example.com'))
    # Original 'From' address is now the Reply-To.
    newmsg['Reply-To'] = msg_components['From']
    newmsg['Subject'] = msg_components['Subject']  # Set the subject to match.
    newmsg['Message-ID'] = msg_components['Message-ID']
    newmsg['Date'] = msg_components['Date']
    # Some lists add these next two headers, only add them if present in original message.
    if list_name and list_name != list_address:
        newmsg['List-Id'] = "{} <{}>".format(list_name, list_address)
    else:
        newmsg['List-Id'] = "<{}>".format(list_address)

    if allow_posts:
        if list_address and list_address != '':
            newmsg['List-Post'] = "<mailto:{}>".format(list_address)

        if moderated:
            newmsg['List-Post'] += " (Postings are Moderated)"
    else:
        newmsg['List-Post'] = "NO (posting not allowed on this list)"

    return newmsg


def from_string(msg_string, list_name, list_address, moderated=False, allow_posts=True):
    """
    Constructs a new DMARC compliant listserv email message object from an existing one in a string-like object.
    :param msg_string: A string-like object containing the original message.
    :param list_name: The long name of the mailing list (for example, "Test List")
    :param list_address: The email address of the mailing list (for example, "list@example.com")
    :param moderated: Optional, specify if posts to the mailing list are moderated. Default is "false"
    :param allow_posts: Optional, specify if posting to the mailing list is permitted. Default is "True"
    :return: A new Message object that contains a DMARC-compliant listserv message ready to be sent out to a list.
    """
    return _construct_dmarc_message(email.message_from_string(msg_string),
                                    list_name, list_address, moderated, allow_posts)


def from_bytes(msg_bytes, list_name, list_address, moderated=False, allow_posts=True):
    """
    Constructs a new DMARC compliant listserv email message object from an existing one in a bytes-like object.
    :param msg_bytes: A bytes-like object containing the original message.
    :param list_name: The long name of the mailing list (for example, "Test List")
    :param list_address: The email address of the mailing list (for example, "list@example.com")
    :param moderated: Optional, specify if posts to the mailing list are moderated. Default is "false"
    :param allow_posts: Optional, specify if posting to the mailing list is permitted. Default is "True"
    :return: A new Message object that contains a DMARC-compliant listserv message ready to be sent out to a list.
    """
    return _construct_dmarc_message(email.message_from_bytes(msg_bytes),
                                    list_name, list_address, moderated, allow_posts)


def from_message(msg_obj, list_name, list_address, moderated=False, allow_posts=True):
    """
    Constructs a new DMARC compliant listserv email message object from an existing email message object.
    :param msg_obj: An instance of email.message.Message containing the original email message.
    :param list_name: The long name of the mailing list (for example, "Test List")
    :param list_address: The email address of the mailing list (for example, "list@example.com")
    :param moderated: Optional, specify if posts to the mailing list are moderated. Default is "false"
    :param allow_posts: Optional, specify if posting to the mailing list is permitted. Default is "True"
    :return: A new Message object that contains a DMARC-compliant listserv message ready to be sent out to a list.
    """
    return _construct_dmarc_message(msg_obj, list_name, list_address, moderated, allow_posts)
