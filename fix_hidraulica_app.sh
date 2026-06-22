#!/bin/bash
sed -i 's/@app.route('\''\/api\/hidraulica'\'', methods=\['\''POST'\''\])\ndef hidraulica():/@app.route('\''\/api\/perda_carga'\'', methods=\['\''POST'\''\])\ndef perda_carga():/' backend/app.py
