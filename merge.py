#!/usr/bin/python
""" Copyright (c) 2012 Fabien Cazenave, Mozilla.
  "
  " Permission is hereby granted, free of charge, to any person obtaining a copy
  " of this software and associated documentation files (the "Software"), to
  " deal in the Software without restriction, including without limitation the
  " rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
  " sell copies of the Software, and to permit persons to whom the Software is
  " furnished to do so, subject to the following conditions:
  "
  " The above copyright notice and this permission notice shall be included in
  " all copies or substantial portions of the Software.
  "
  " THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  " IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  " FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  " AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  " LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
  " FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
  " IN THE SOFTWARE.
  """

# Warning: I suck at writing Python, and this code has be done really quickly.
import json
import os
import shutil
import sys

def main():
  outputdir = '/home/kaze/Documents/mozilla/gaia/apps'
  baseLocale = 'en-US'
  supportedApps = os.listdir(baseLocale)
  supportedLocales = ['ar', 'en-US', 'fr', 'ru', 'zh-TW']

  for app in supportedApps:

    destDir = os.path.join(outputdir, app)
    if not os.path.isdir(destDir):
       os.makedirs(destDir)

    # inject localized name/descriptions into JSON manifests
    destPath = os.path.join(destDir, 'manifest.json')
    print(destPath)

    # load JSON manifest
    dest = open(destPath, 'r')
    data = json.load(dest)
    data['locales'] = {}
    data['default_locale'] = 'en-US'
    dest.close()

    # fill the 'locales' property
    for lang in supportedLocales:
      sourcePath = os.path.join(lang, app, 'manifest.properties')
      source = open(sourcePath, 'r');

      # parse name/description in the properties file -- FIXME:
      # we assume to find 'name' on the first line, 'description' on the 2nd
      desc = {}
      lines = source.readlines()
      desc['name'] = lines[0].replace('name=', '').replace('\n', '')
      desc['description'] = lines[1].replace('description=', '').replace('\n', '')
      data['locales'][lang] = desc

      dest = open(destPath, 'wb')
      dest.write(json.dumps(data, indent = 2, separators=(',', ': ')))
      dest.close()

    # concatenate files in the 'locale' directory (if any)
    localeDir = os.path.join(baseLocale, app, 'locale')
    if os.path.isdir(localeDir):
      #destLocaleDir = os.path.join(destDir, 'locale')
      #print(destLocaleDir)
      for resource in os.listdir(localeDir):
        destPath = os.path.join(destDir, 'locale', resource)
        print(destPath)
        #dest = open(os.path.join(destLocaleDir, resource), 'wb')
        dest = open(destPath, 'wb')
        for lang in supportedLocales:
          dest.write('[' + lang + ']\n')
          sourcePath = os.path.join(lang, app, 'locale', resource)
          shutil.copyfileobj(open(sourcePath, 'rb'), dest)

# startup
if __name__ == "__main__":
  main()

