import json
import csv
import datetime
import dateutil.parser

now = datetime.datetime.utcnow()

def listCommittees(committee):
    start_date  = dateutil.parser.parse(committee.get('start'))
    end_date  = dateutil.parser.parse(committee.get('end'))

    if now > end_date:
        return None

    if committee.get('role') != 'Substitute':
        return committee.get('abbr')

def formatMEPs(mep):
    if not(mep.get('active')):
        return

    committees = [listCommittees(committee) for committee in mep.get('Committees', {})]
    committees = list(dict.fromkeys(filter(None.__ne__, committees)))

    return {
        'userID'       : mep.get('UserID'),
        'name_full'    : mep.get('Name', {}).get('full'),
        'name_first'   : mep.get('Name', {}).get('sur'),
        'name_last'    : mep.get('Name', {}).get('family'),
        'photo_url'    : mep.get('Photo'),
        'group'        : next(iter(mep.get('Groups', {})), {}).get('groupid'),
        'group_role'   : next(iter(mep.get('Groups', {})), {}).get('role'),
        'country'      : mep.get('Constituencies', {})[0].get('country'),
        'committees'   : committees,
        'gender'       : mep.get('Gender'),
        'phone_bru'    : mep.get('Addresses', {}).get('Brussels', {}).get('Phone'),
        'office_bru'   : mep.get('Addresses', {}).get('Brussels', {}).get('Address', {}).get('Office'),
        'phone_stb'    : mep.get('Addresses', {}).get('Strasbourg', {}).get('Phone'),
        'office_stb'   : mep.get('Addresses', {}).get('Strasbourg', {}).get('Address', {}).get('Office'),
        'email'        : mep.get('Mail'),
        'website'      : mep.get('Homepage'),
        'facebook'     : mep.get('Facebook'),
        'instagram'    : mep.get('Instagram'),
        'twitter'      : mep.get('Twitter'),
        'salutation_de': 'Sehr geehrter Herr MdEP ' + mep.get('Name', {}).get('full') if mep.get('Gender') == 'M' else 'Sehr geehrte Frau MdEP ' + mep.get('Name', {}).get('full'),
        'salutation_en': 'Dear MEP ' + mep.get('Name', {}).get('full')
    }

with open('ep_meps.json', 'r') as f:
    mep_data = json.load(f)

meps = [formatMEPs(mep) for mep in mep_data]
meps = list(filter(None.__ne__, meps))

with open("ep_meps.csv", "w", newline="") as f:
    fieldnames = ['userID', 'name_full', 'name_first', 'name_last',
        'photo_url', 'group', 'group_role', 'country', 'committees',
        'gender', 'phone_bru', 'office_bru', 'phone_stb', 'office_stb',
        'email', 'website', 'facebook', 'instagram', 'twitter',
        'salutation_de', 'salutation_en']

    writer = csv.DictWriter(f, fieldnames)

    writer.writeheader()
    writer.writerows(meps)
