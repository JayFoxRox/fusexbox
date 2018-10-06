#!/usr/bin/env python3

#FIXME: Add license

# See README.md for license information


#FIXME: Probably not necessary?
from __future__ import print_function, absolute_import, division

import logging
import stat

from xboxpy import *

from errno import ENOENT

from fuse import FUSE, FuseOSError, Operations, LoggingMixIn

from fusexbox import *

class XbdmError(Exception):
  def __init__(self, status=0):
    self.status = status

class XbdmUnexpectedError(XbdmError): pass
class XbdmMaxNumberOfConnectionsExceeded(XbdmError): pass
class XbdmFileNotFoundError(XbdmError): pass

def xbdm(command, arguments={}, data=None, length=None):
  if len(arguments) > 0:
    command += ' ' + xbdm_create_keys(arguments)
  status, response = interface.if_xbdm.xbdm_command(command, data, length)
  
  if status in [200, 201, 202, 203, 204, 205]:
    return response
  elif status == 402:
    raise XbdmFileNotFoundError()
  else:
    assert(status // 100 == 4)
    raise XbdmError(status)

def escape_xbdm_string(name):
  name = name.replace('"', '\\"')
  return '"%s"' % name

def unix_to_xbox_path(unix_path):
  assert(unix_path[0] == '/')
  print(len(unix_path))
  if len(unix_path) >= 3:
    assert(unix_path[2] == '/')
    path = unix_path[3:].replace('/', '\\')
  else:
    path = ''
  drive = unix_path[1]
  xbox_path = '%s:\\%s' % (drive, path)
  return xbox_path

def parse_xbdm_keys(string):
  return interface.if_xbdm.xbdm_parse_keys(string)

def get_xbdm_hilo(keys, key):
  return (keys[key + 'hi'] << 32) | keys[key + 'lo']

#FIXME: If this would return python timestamps, this should be in the xboxpy xbdm interface?
def get_xbdm_date(keys, key):
  filetime = get_xbdm_hilo(keys, key)
  if filetime == 0:
    return 0
  return filetime // 10000000 - 11644473600

#FIXME: Move to xbdm interface
def xbdm_create_keys(keys):
  string = ''
  for key, value in keys.items():
    #FIXME: Add support for QWORD
    if isinstance(value, int):
      string += ' %s=0x%X' % (key, value)
    elif isinstance(value, str):
      string += ' %s=%s' % (key, escape_xbdm_string(value))
    elif isinstance(value, bool):
      if value == True:
        string += ' %s' % key
    else:
      assert(False)
  return string[1:]

#FIXME: Add another class which uses the xboxpy CALL api to re-create this interface
class Xbdm():

  def drivelist(self):
    return list(xbdm('drivelist'))

  def dirlist(self, name):
    raw_files = xbdm('dirlist name=%s' % escape_xbdm_string(name))
    files = []
    for raw_file in raw_files:
      keys = parse_xbdm_keys(raw_file)
      file = {}
      file['name'] = keys['name']
      file['size'] = get_xbdm_hilo(keys, 'size')
      file['create'] = get_xbdm_date(keys, 'create')
      file['change'] = get_xbdm_date(keys, 'change')
      files.append(file)
    return files

  def getfileattributes(self, name):
    raw_file = xbdm('getfileattributes name=%s' % escape_xbdm_string(name))
    assert(len(raw_file) == 1)
    keys = parse_xbdm_keys(raw_file[0])
    file = {}
    file['size'] = get_xbdm_hilo(keys, 'size')
    file['create'] = get_xbdm_date(keys, 'create')
    file['change'] = get_xbdm_date(keys, 'change')
    file['directory'] = keys.get('directory', False)
    file['readonly'] = keys.get('readonly', False)
    file['hidden'] = keys.get('hidden', False)
    return file

  def getfile(self, name, offset=None, size=None):
    arguments = {}
    arguments['name'] = name
    if offset is not None:
      arguments['offset'] = offset
    if size is not None:
      arguments['size'] = size
    return xbdm('getfile', arguments, length=0)

  #FIXME: setfileattributes
  #FIXME: delete
  def delete(self, name, dir=None):
    arguments = {}
    arguments['name'] = name
    if dir is not None:
      arguments['dir'] = dir
    return xbdm('delete', arguments)   

  def mkdir(self, name):
    arguments = {}
    arguments['name'] = name
    return xbdm('mkdir', arguments)

  def rename(self, newname, name):
    arguments = {}
    arguments['newname'] = newname
    arguments['name'] = name
    return xbdm('rename', arguments)

  #FIXME: sendfile
  def sendfile(self, name, data):
    arguments = {}
    arguments['name'] = name
    arguments['length'] = len(data)
    return xbdm('sendfile', arguments, data=data)

  def magicboot(self, title, debug=None):
    arguments = {}
    arguments['title'] = title
    if debug is not None:
      arguments['debug'] = debug
    return xbdm('magicboot', arguments)


class FuseXbox(LoggingMixIn, Operations):
    '''
    fusepy backend for talking to an original Xbox using the XBDM protocol
    from the Microsoft Xbox Development Kit.
    '''

    def __init__(self, xbdm):
        #self.sftp = self.client.open_sftp()
        print('init')
        self.xbdm = xbdm

    def chmod(self, path, mode):
        print('chmod')
        #FIXME: Implement read-only attribute
        return 0
        #return self.sftp.chmod(path, mode)

    def create(self, path, mode):
        #f = self.sftp.open(path, 'w')
        #f.chmod(mode)
        #f.close()
        print('create')

        self.xbdm.sendfile(unix_to_xbox_path(path), bytes([]))

        return 0

    def destroy(self, path):
        #self.sftp.close()
        #self.client.close()
        print('destroy')

    def getattr(self, path, fh=None):
        #try:
        #    st = self.sftp.lstat(path)
        #except IOError:
        #    raise FuseOSError(ENOENT)
        #
        #return dict((key, getattr(st, key)) for key in (
        #    'st_atime', 'st_gid', 'st_mode', 'st_mtime', 'st_size', 'st_uid'))
        print('getattr(%s)' % path)

        permissions = 0o777

        if path == '/':
          return {
            'st_mode': stat.S_IFDIR | permissions
          }

        try:
          attr = self.xbdm.getfileattributes(unix_to_xbox_path(path))
        except XbdmFileNotFoundError:
          raise FuseOSError(ENOENT)

        if attr['readonly']:
          permissions &= ~0o222
        if attr['hidden']:
          # macOS has some "hidden" flag, that might be re-usable.
          # Using dot-files is a bad idea because it would be very confusing.
          pass
          
        print(attr)
        return {
          'st_mode': (stat.S_IFDIR if attr['directory'] else stat.S_IFREG) | permissions,
          'st_size': attr['size'],
          'st_mtime': attr['create'],
          'st_ctime': attr['change']
        }

    def mkdir(self, path, mode):
        #return self.sftp.mkdir(path, mode)
        print('mkdir')
        self.xbdm.mkdir(unix_to_xbox_path(path))
        return 0

    def read(self, path, size, offset, fh):
        return self.xbdm.getfile(unix_to_xbox_path(path), offset=offset, size=size)

    def readdir(self, path, fh):
        #return ['.', '..'] + [name.encode('utf-8')
        #                      for name in self.sftp.listdir(path)]
        print('readdir(%s)' % path)

        if path == '/':
          return ['.', '..'] + self.xbdm.drivelist()
        else:
          return ['.', '..'] + [e['name'] for e in self.xbdm.dirlist(unix_to_xbox_path(path))]

    #FIXME: Should not be necessary
    def readlink(self, path):
        #return self.sftp.readlink(path)
        print('readlink')

    def rename(self, old, new):
        #return self.sftp.rename(old, new)
        print('rename(%s, %s)' % (old, new))
        new_xbox_path = unix_to_xbox_path(new)
        self.xbdm.delete(new_xbox_path)
        self.xbdm.rename(new_xbox_path, unix_to_xbox_path(old))
        return 0

    def rmdir(self, path):
        #return self.sftp.rmdir(path)
        print('rmdir(%s)' % path)
        self.xbdm.delete(unix_to_xbox_path(path), dir=True)
        return 0

    def truncate(self, path, length, fh=None):
        #return self.sftp.truncate(path, length)
        print('truncate')

        #FIXME: Find a faster alternative for this
        xbox_path = unix_to_xbox_path(path)
        old_data = self.xbdm.getfile(xbox_path)
        if len(old_data) != length:
          self.xbdm.sendfile(xbox_path, old_data[0:length])

    def unlink(self, path):
        #return self.sftp.unlink(path)
        print('unlink(%s)' % path)
        self.xbdm.delete(unix_to_xbox_path(path))

    def utimens(self, path, times=None):
        #return self.sftp.utime(path, times)
        print('utimens')
        #FIXME: Set file attributes
        #FIXME: Get the current time on xbox

    def write(self, path, data, offset, fh):
        print('write(%s, %d bytes, %d)', path, len(data), offset)

        #FIXME: Find a faster alternative for this:
        #       There could be a cache, so if this is written in chunks,
        #       we don't have to re-read it every time.
        #FIXME: Add support for writefile on XBDM >= 4531
        xbox_path = unix_to_xbox_path(path)
        #FIXME: Receive old data in 2 chunks, so we don't transfer data we'll
        #       overwrite anyway.
        old_data = self.xbdm.getfile(xbox_path)
        new_data = old_data[0:offset] + data + old_data[offset+len(data):]
        self.xbdm.sendfile(xbox_path, new_data)

        return len(data)

    def ioctl(self, path, cmd, arg, fh, flags, data):
      if cmd == XBOXIOCRUN:
        self.xbdm.magicboot(unix_to_xbox_path(path), debug=True)
      else:
        raise FuseOSError(ENOTTY)
      return 0


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('mount')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    fuse = FUSE(
        FuseXbox(Xbdm()),
        args.mount,
        foreground=True,
        nothreads=True,
        allow_other=False)
