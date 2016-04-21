#!/bin/bash
git submodule foreach git pull
cp mockups/assets/citadel.css ntusa/static/
git add mockups ntusa/static/
git commit -m "Update newest style from mockup upstream"
