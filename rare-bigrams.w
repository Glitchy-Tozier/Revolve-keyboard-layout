#!/usr/bin/env bash
# -*- wisp -*-
exec -a "$0" guile -L "$(dirname "$(realpath "$0")")" -x .w --language=wisp -e '(rare-bigrams)' -c '' "$@"
;; !#

define-module : rare-bigrams
    . #:export : main

import : srfi srfi-1
         ice-9 rdelim

define : usage . args
    format (current-error-port) "~a <2-gram-file.txt>"

define : main args
    when : null? : cdr args
           apply usage args
           exit 1
    let : : port : open-input-file : second args
        define seen-map : make-hash-table 10000
        define : select-canonical-bigram line
            list->string
              stable-sort
                string->list
                  string-downcase
                      string-join
                          cdr : string-split line #\space
                          . " "
                . char<?
        define : unknown? bigram
            not : hash-ref seen-map bigram
        define simple-lowercase-german-regexp
            make-regexp "^[abcdefghijklmnopqrstuvwxyzäöüß]+$"
        define : simple-lowercase-german? bigram
            regexp-exec simple-lowercase-german-regexp bigram
        define sorted-bigrams
            let loop : (line (read-line port)) (unique (list))
                 if : eof-object? line
                      reverse unique
                      loop (read-line port)
                          let : : bigram : select-canonical-bigram line
                             if : unknown? bigram
                                 begin
                                     hash-set! seen-map bigram #t
                                     if : simple-lowercase-german? bigram
                                          cons bigram unique
                                          . unique
                                 . unique
        map : λ(x) : format #t "~a\n" x
            . sorted-bigrams
