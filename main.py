#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from helper.helper import Database


logging.basicConfig(level=logging.INFO)


if  __name__ == "__main__":
    logging.info("Staring database...")
    database = Database()
    while database.apply(input('>>> ')):
        pass
