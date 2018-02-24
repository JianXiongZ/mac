# -*- coding: utf-8; -*-

import mysql.connector
import logging
import time

class DataBase():
    def __init__(self, db):
        self.user = db['user']
        self.database = db['database']
        self.passwd = db['password']
        self.host = db['host']
        self.con = None
        self.log = logging.getLogger('PRODUCT.SQL')

    def connect(self):
        self.con = mysql.connector.connect(
	    user=self.user, 
	    database=self.database, 
	    passwd=self.passwd,
	    host=self.host)

        self.cursor = self.con.cursor()

    def commit(self):
        self.con.commit()

    def disconnect(self):
        self.cursor.close()
        self.con.close()

    def _create(self, name, column_def, additional=None, suffix=None):
        self.query = 'CREATE TABLE IF NOT EXISTS `{}` ({}{}){}'.format(
            name,
            ', '.join('`{name}` {type}'.format(**c) for c in column_def),
            ', {}'.format(additional) if additional else '',
            ' {}'.format(suffix) if suffix else ''
        )
        self.value = None

    def _insert(self, name, column, value):
        self.query = 'INSERT INTO `{}` (`{}`) VALUES ({})'.format(
            name,
            '`, `'.join(column),
            ', '.join('%s' for i in range(len(value)))
        )
        self.value = value
		

    def _select(self, name, column=None, clause=None, value=None):
        self.query = 'SELECT {} FROM `{}`{}'.format(
            '`{}`'.format('`, `'.join(column)) if column else '*',
            name,
            ' WHERE {}'.format(clause) if clause else ''
        )
        self.value = value

    def _raw(self, query, value=None):
        self.query = query
        self.value = value

    def run(self, command, *args, **kwargs):
        if command == 'create':
            self._create(*args, **kwargs)
        elif command == 'insert':
            self._insert(*args, **kwargs)
        elif command == 'select':
            self._select(*args, **kwargs)
        elif command == 'raw':
            self._raw(*args, **kwargs)
        else:
            self.log.error('Unknown sql command: {}'.format(command))
            return False

        try:
            self.cursor.execute(self.query, self.value)
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as e:
            if 'No result set to fetch from.' in str(e):
                return True
            self.log.error(str(e))
            self.log.debug(self.query)
            if self.value is not None:
                self.log.debug(self.value)
            return False
