# coding=utf-8


# noinspection PyTypeChecker
def dict_from_string(dispstr):
    # type: (str) -> dict

    """
    Converts a string which contains a Content-Disposition
    header's contents into a dict.
    :param dispstr: String with Content-Disposition value
    :return: Dictionary of Content-Disposition values.
    """
    # Example input: 'attachment;\n filename="test.doc"'
    disp_parts = dispstr.split(';')
    disp_dict = {}
    # returns: ['attachment', '\n filename="test.doc"']
    for d_part in disp_parts:
        if len(d_part.split('=', 1)) > 1:
            # First, clean up the individual segments of the parameters and store them as 'cleaned'
            disp_param_cleaned = list(map(str.strip, d_part.split('=', 1)))
            # Now, create the dict entry.
            disp_dict[disp_param_cleaned[0]] = disp_param_cleaned[1]
        else:
            disp_dict[d_part.strip().lower()] = None

    # Example output: {'attachment': None, 'filename': '"test.doc"'}
    # Also valid output: {'filename': '"test.doc"', 'attachment': None}

    return disp_dict
