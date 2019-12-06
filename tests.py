# coding=utf-8
import datetime
import dmarcmsg.construct
import email.message
from email.mime.text import MIMEText
import email.utils as mailutil
import unittest


# Helper function to generate the same or relatively same message each time before passing into
# DMARCMSG
def _generate_standard_test_message(to_: str = "noreply@nonexistent.tld",
                                    from_: str = "test@nonexistent.tld",
                                    subject_: str = "Testing 123") -> email.message.Message:
    msg = MIMEText("Test Message 123")
    msg['To'] = to_
    msg['From'] = from_
    msg['Subject'] = subject_
    msg['Date'] = mailutil.format_datetime(datetime.datetime.utcnow())
    msg['Message-ID'] = mailutil.make_msgid()
    return msg


# Tests to verify DMARCMSG works properly.
# noinspection PyMissingTypeHints
class TestDMARCMSG(unittest.TestCase):
    msg = _generate_standard_test_message()
    dmarc = dmarcmsg.construct.from_message(msg, list_address='list@nonexistent.tld',
                                            list_name="MailingList")

    def assert_messages_exist(self):
        self.assertIsNotNone(self.dmarc)
        self.assertIsInstance(self.dmarc, email.message.Message)

    def test_from_conversion(self):
        self.assertIn(self.msg['From'], self.dmarc['From'])

    def test_only_one_date(self):
        self.assertEqual(len(self.dmarc.get_all('Date')), 1)

    def test_dates_match(self):
        self.assertEqual(self.msg['Date'], self.dmarc['Date'])

    def test_replyto(self):
        self.assertIn(mailutil.parseaddr(self.msg['From'])[1], self.dmarc['Reply-To'])

    def test_subjects_match(self):
        self.assertEqual(self.msg['Subject'], self.dmarc['Subject'])

    def test_messageids_unique(self):
        self.assertNotEqual(self.msg['Message-ID'], self.dmarc['Message-ID'])
