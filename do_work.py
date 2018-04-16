#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import uuid
import logging
import config_web
import xlrd

import app.models.base_model as base_model


def main():
    FORMAT = "%(asctime)s - %(message)s"
    logging.basicConfig(format=FORMAT)
    logging.getLogger().setLevel("INFO".upper())

    if len(sys.argv) > 1:

        if sys.argv[1] == 'tmp_dist':
            import app.workers.order_worker as order_worker
            order_worker._tmp_dist_orders()


        # --- go sched --- #

        if sys.argv[1] == "sched":
            import app.workers.sched_worker as sched_worker
            sched_worker.run()


if __name__ == "__main__":
    main()
