#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018,2019 Abacus Technologies, Inc.
# Copyright (c) 2018,2019 Fumiyuki Shimizu
# MIT License: https://opensource.org/licenses/MIT

import os
import re

import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot
from matplotlib import gridspec
            
def main():
    log_file = os.path.join('backup', 'train.out')
    output_file_loss_png = os.path.join('backup', 'loss.png')
    if not os.path.exists(log_file):
        raise FileNotFoundError(log_file)
    col_iter = 'iter.'
    col_loss = 'loss'
    col_loss_avg = 'loss avg.'
    df = pd.DataFrame(columns=( col_iter, col_loss, col_loss_avg ))

    x = 0
    it = 0
    it_last = 0
    regexp = re.compile(r'^(\d+)\s*:\s*([.\d]+)\s*,\s*([.\d]+)\s*avg\s*,')
    print('{}:'.format(log_file), flush=True, end='')
    with open(log_file, 'r') as f:
        for line in f:
            m = regexp.match(line)
            if m:
                it = int(m.group(1))
                if it_last > it:
                    df = df.loc[df[col_iter]<it]
                it_last = it
                df = pd.concat(( df, pd.DataFrame.from_dict({
                    col_iter: ( it, ),
                    col_loss    : ( float(m.group(2)), ),
                    col_loss_avg: ( float(m.group(3)), ),
                }) ), sort=False)

                x = (x + 1) % 300
                if 0 == x:
                    print('.', flush=True, end='')
    print('')
    df.sort_values(col_iter, ascending=True, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.set_index(col_iter, inplace=True)

    fig = pyplot.figure(figsize=(5, 5), dpi=150)
    try:
        gs = gridspec.GridSpec(3, 2)
        ax1 = fig.add_subplot(gs[0, :])
        ax2 = fig.add_subplot(gs[1, 0])
        ax3 = fig.add_subplot(gs[1, 1])
        ax4 = fig.add_subplot(gs[2, 0])
        ax5 = fig.add_subplot(gs[2, 1])
        #ax2.set_ylim(bottom=0  , top=5)
        #ax3.set_ylim(bottom=0.5, top=1)
        #ax4.set_ylim(bottom=0.5, top=0.8)
        ax1.grid(True)
        ax2.grid(True)
        ax3.grid(True)
        ax4.grid(True)
        ax5.grid(True)
        df                     .plot(ax=ax1)
        if 2000 < it_last:
            df.iloc[     :  500, :].plot(ax=ax2)
            df.iloc[  500: 2000, :].plot(ax=ax3)
            df.iloc[ 2000:     , :].plot(ax=ax4)
            df.iloc[-2000:     , :].plot(ax=ax5)
        else:
            w = it_last / 3
            df.iloc[         :int(w)  , :].plot(ax=ax2)
            df.iloc[         :int(2*w), :].plot(ax=ax3)
            df.iloc[   int(w):int(2*w), :].plot(ax=ax4)
            df.iloc[ int(2*w):        , :].plot(ax=ax5)
        fig.tight_layout()
        fig.savefig(output_file_loss_png)
    finally:
        pyplot.close(fig)

if __name__ == '__main__':
    main()

# end of file
