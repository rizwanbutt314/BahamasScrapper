import mysql.connector
import datetime
import dateparser
import constants


def database_connection():
    con = mysql.connector.connect(user=constants.DATABASE_USER, password=constants.DATABASE_PASSWORD, database=constants.DATABASE_NAME)
    cur = con.cursor(buffered=True)
    return con, cur


def insert_data(data, bulk_insert=False):
    con, cur = database_connection()

    if bulk_insert:
        sql = """INSERT INTO legislations(short_title, short_title_slug, type, year, number, notes, url, commenced_date, status, migrated, created_at)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        number_of_rows = cur.executemany(sql, data)

    con.commit()
    con.close()


def check_categroy(con, cur, category):
    sql = """select id from categories where name='{0}'""".format(category)
    cur.execute(sql)
    row = cur.fetchone()

    return row


def insert_category(con, cur, category):
    created_at  = datetime.datetime.now()
    sql = """INSERT INTO categories(name, created_at)
        VALUES(%s, %s)"""
    cur.execute(sql, (category, created_at))


def handle_category(category):
    con, cur = database_connection()
    category_exists = check_categroy(con, cur, category)

    category_id = None
    if category_exists:
        category_id = category_exists[0]
    else:
        insert_category(con, cur, category)
        category_again_exists = check_categroy(con, cur, category)
        category_id = category_again_exists[0]

    con.commit()
    con.close()
    return category_id


def check_legistation(con, cur, year, number):
    sql = """select * from legislations where year={0} and number={1}""".format(year, number)
    cur.execute(sql)
    row = cur.fetchone()

    return row


def insert_legistation(con, cur, data):
    sql = """INSERT INTO legislations(short_title, short_title_slug, type, year, number, notes, url, commenced_date, status, migrated, created_at,category_id)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    cur.execute(sql, data)


def update_legistation(con, cur, legistation_id, category_id):
    updated_at  = datetime.datetime.now()
    sql = """UPDATE legislations
       SET category_id=%s, updated_at=%s
       WHERE id={0}""".format(legistation_id)

    cur.execute(sql, (category_id, updated_at))


def handle_legistation(category_id, parsed_data):
    con, cur = database_connection()
    del parsed_data[-1]
    parsed_data.append(category_id)
    legistation_exists = check_legistation(con, cur, parsed_data[3], parsed_data[4])

    legistation_id = None
    legistation_type = ""
    if legistation_exists:
        legistation_id = legistation_exists[0]
        legistation_type = legistation_exists[4]
        update_legistation(con, cur, legistation_id, category_id)   #updating legistation
    else:
        insert_legistation(con, cur, tuple(parsed_data))    #inserting new legistation
        legistation_again_exists = check_legistation(con, cur, parsed_data[3], parsed_data[4])
        legistation_id = legistation_again_exists[0]
        legistation_type = legistation_again_exists[4]

    con.commit()
    con.close()
    return (legistation_id, legistation_type)


def handle_amendments(legistation_id, title, legistation_type):
    created_at  = datetime.datetime.now()

    con, cur = database_connection()
    sql = ""

    if 'amended by...' in title:
        sql = """INSERT INTO principal_amendment(principal_id, amendment_id, created_at)
            VALUES(%s, %s, %s)"""
    elif 'amended by...' not in title and legistation_type !='SUBORDINATE':
        sql = """INSERT INTO principal_subsidiary(principal_id, subsidiary_id, created_at)
            VALUES(%s, %s, %s)"""
    elif 'amended by...' not in title and legistation_type =='SUBORDINATE':
        sql = """INSERT INTO subsidiary_amendment(amendment_id, subsidiary_id, created_at)
            VALUES(%s, %s, %s)"""

    cur.execute(sql, (legistation_id, legistation_id, created_at))
    con.commit()
    con.close()


def update_repeal_legistation(con, cur, legistation_id, repeal_date):
    updated_at  = datetime.datetime.now()
    sql = """UPDATE legislations
       SET status='Repealed', updated_at=%s, repealed_date=%s
       WHERE id={0}""".format(legistation_id)

    cur.execute(sql, (updated_at, repeal_date))