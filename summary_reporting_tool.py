#!/usr/bin/env python3

"""
Logs Analysis Project:

This reporting tool builds an informative summary from the news database.
The report measures article and author popularity as well as days that the site
experiences a high amount of user request errors.

USAGE:    ./summary_reporting_tool.py

OUTPUT:  Results are printed to screen as well as to logfile in
         current directory.
"""

import psycopg2
import string
import time


def connect(database_name='news'):
    """
    Connect to the PostgreSQL database.
    Returns a database connection.
    """
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        print("Unable to connect to database")
        sys.exit(1)


def fetch_query(query):
    """
    Connect to the database, execute query,
    fetch results, close connection, return results
    """
    db, c = connect()
    c.execute(query)
    results = c.fetchall()

    db.close()
    return results


def print_top_articles(top_n=None, PRINT_TO_SCREEN=True):
    """
    Sum up the views of each article and sort them by views (most to least)
    """
    title = '\nMost popular articles of all time:\n'
    template = '   "$article" — $views views\n'
    query = "SELECT articles.title, views.views \
            FROM articles, \
            (SELECT path, COUNT(path) AS views \
            FROM log \
            WHERE status LIKE '%200%' \
            GROUP BY path) as views \
            WHERE views.path = '/article/' || articles.slug \
            ORDER BY views.views DESC;"

    if top_n and isinstance(top_n, int) and top_n > 0:
        title = title[:14] + str(top_n) + ' ' + title[14:]
        query += query[:-1] + " LIMIT {};".format(top_n)

    fetch_results = fetch_query(query)
    top_articles = ({'article': str(row[0]), 'views': str(row[1])}
                    for row in fetch_results)

    results = printer(title=title, parser=template, entries=top_articles)
    if PRINT_TO_SCREEN:
        print(results)
    return results


def print_top_authors(top_n=None, PRINT_TO_SCREEN=True):
    """
    Sum up article views by author and sort them by views (most to least)
    """
    title = '\nMost popular authors of all time:\n'
    template = '    $author — $views views\n'
    query = "SELECT authors.name, page_views \
            FROM authors, \
            (SELECT articles.author, COUNT(articles.author) as page_views \
            FROM articles \
            JOIN log ON log.path = '/article/' || articles.slug \
            GROUP BY (articles.author)) as views \
            WHERE authors.id = views.author \
            ORDER BY page_views DESC;"

    if top_n and isinstance(top_n, int) and top_n > 0:
        title = title[:14] + str(top_n) + ' ' + title[14:]
        query += query[:-1] + " LIMIT {};".format(top_n)

    fetch_results = fetch_query(query)
    top_authors = ({'author': str(row[0]), 'views': str(row[1])}
                   for row in fetch_results)

    results = printer(title=title, parser=template, entries=top_authors)
    if PRINT_TO_SCREEN:
        print(results)
    return results


def print_top_error_days(threshold=1.0, PRINT_TO_SCREEN=True):
    """
    Find days which experienced requests errors that met/exceeded threshold %
    """
    if not(threshold and (isinstance(threshold, float) or
       isinstance(threshold, int)) and threshold >= 0.00 and
       threshold <= 100.0):
        threshold = 1.0

    months_str = 'January February March April May June July August September \
                 October November December'
    month_mapper = {num+1: month for num, month in
                    enumerate(months_str.split())}

    title = '\nDays on which more than {}% of requests led to errors:\
                 \n'.format(threshold)
    template = '    $month $day, $year — $req_err_percent% errors\n'
    query = "SELECT EXTRACT(YEAR FROM log.time) as year, \
            EXTRACT(MONTH FROM log.time) as month, \
            EXTRACT(DAY FROM log.time) AS day, \
            ROUND((err.errors*100/req.requests::numeric), 2) \
            as percent_req_err \
            FROM log, \
            (SELECT date_trunc('day', log.time) AS timestamp, \
            COUNT(date_trunc('day', log.time)) AS requests \
            FROM log \
            GROUP BY timestamp) AS req, \
            (SELECT date_trunc('day', log.time) AS timestamp, \
            COUNT(date_trunc('day', log.time)) AS errors \
            FROM log \
            WHERE status = '404 NOT FOUND' \
            GROUP BY timestamp) AS err \
            WHERE date_trunc('day', log.time) = req.timestamp AND \
                  date_trunc('day', log.time) = err.timestamp AND \
                  err.errors/req.requests::float >= {0} \
            GROUP BY year, month, day, err.errors, req.requests \
            ORDER BY year, month, day;".format(threshold/100)

    fetch_results = fetch_query(query)
    errors = ({'year': str(int(row[0])), 'month': month_mapper[int(row[1])],
              'day': str(int(row[2])), 'req_err_percent': str(float(row[3]))}
              for row in fetch_results)

    results = printer(title=title, parser=template, entries=errors)
    if PRINT_TO_SCREEN:
        print(results)
    return results


def timestamp_gen(file_extension=False):
    """
    Generate the current UTC time in <YYYY-MM-DD_HH:MM:SS_UTC> format as str
    """
    time_format = '_%Y-%m-%d_%H:%M:%S_UTC.log'
    if not file_extension:
        time_format = time_format[1:-4]

    utc_time_tuple = time.gmtime(time.time())
    utc_timestamp = time.strftime(time_format, utc_time_tuple)
    return utc_timestamp


def report_init(report_name='SUMMARY_REPORT'):
    """
    Create report file with appended timestamp
    """
    file_name = report_name + timestamp_gen(file_extension=True)

    def report_builder(lines):
        with open(file_name, 'a') as file_obj_out:
            for line in lines:
                file_obj_out.write(line)

    report_builder('{} - {}\n'.format(timestamp_gen(), report_name.title()))
    return report_builder


def printer(title, parser, entries):
    """
    use parser to format entries and return results
    """
    error_msg = '\n{} - Error formatting to template\nENTRY: {}\nPARSER: {}\n'
    results = title
    template = string.Template(parser)
    for entry in entries:
        try:
            results += template.safe_substitute(entry)
        except ValueError as e:
            results += error_msg.format(timestamp_gen(), entry, parser)
    return results


def main():
    """
    Analyze news table and generate report
    """
    report_writer = report_init(report_name='SUMMARY_REPORT')

    report_writer(print_top_articles(top_n=3))
    report_writer(print_top_authors())
    report_writer(print_top_error_days(threshold=1.0))


if __name__ == '__main__':
    main()
