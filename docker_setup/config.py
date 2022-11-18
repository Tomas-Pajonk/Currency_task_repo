import configparser


def config(filename="database.ini", section="postgresql"):
    parser = configparser.ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception("Section {0} is not found in tje {1} file.".format(section, filename))

    return db


config()
