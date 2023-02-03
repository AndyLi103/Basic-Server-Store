################### 
# Course: CSE 138
# Quarter: Winter 2023
# Assignment: #2
# Author: Amin Karbas <mkarbasf@ucsc.edu>
###################

import unittest
import requests

localhost = "localhost" # Docker Toolbox users should use Docker's ip address here
port = 13800
url = 'http://{}:{}/kvs'.format(localhost, port)
keys = ['k1', 'key2']
vals = ['v1', 'val2']

def get(key):
  return requests.get(url+'?key={}'.format(key))

def put(key, val):
  return requests.put(url, json={'key': key, 'val': val})

def delete(key):
  return requests.delete(url+'?key={}'.format(key))


class TestAssignment2(unittest.TestCase):
  
  # Setup: clear all previous values, if they exist
  def setUp(self):
    for k in keys:
      delete(k)


  # Malformed put
  def test_malformed_put(self):
    res = requests.put(url, json={'k': keys[0], 'v': vals[0]})
    self.assertEqual(res.status_code, 400, msg='Did not return status 400 (malformed put)')
    json_body = res.json() # Exception if not parsable to json
    self.assertIn('error', json_body, msg='Key "error" not in json response (malformed put)')
    self.assertEqual(json_body['error'], 'bad PUT', msg='Bad error message (malformed put)')


  # Malformed get
  def test_malformed_get(self):
    res = requests.get(url)
    self.assertEqual(res.status_code, 400, msg='Did not return status 400 (malformed get)')
    json_body = res.json() # Exception if not parsable to json
    self.assertIn('error', json_body, msg='Key "error" not in json response (malformed get)')
    self.assertEqual(json_body['error'], 'bad GET', msg='Bad error message (malformed get)')


  # Malformed delete
  def test_malformed_delete(self):
    res = requests.delete(url)
    self.assertEqual(res.status_code, 400, msg='Did not return status 400 (malformed delete)')
    json_body = res.json() # Exception if not parsable to json
    self.assertIn('error', json_body, msg='Key "error" not in json response (malformed delete)')
    self.assertEqual(json_body['error'], 'bad DELETE', msg='Bad error message (malformed delete)')


  # Put oversized key
  def test_put_oversized_key(self):
    res = put('a'*201, vals[0])
    self.assertEqual(res.status_code, 400, msg='Did not return status 400 (put oversized key)')
    json_body = res.json() # Exception if not parsable to json
    self.assertIn('error', json_body, msg='Key "error" not in json response (put oversized key)')
    self.assertEqual(json_body['error'], 'key or val too long', msg='Bad error message (put oversized key)')


  # Put oversized value
  def test_put_oversized_value(self):
    res = put(keys[0], 'a'*201)
    self.assertEqual(res.status_code, 400, msg='Did not return status 400 (put oversized value)')
    json_body = res.json() # Exception if not parsable to json
    self.assertIn('error', json_body, msg='Key "error" not in json response (put oversized value)')
    self.assertEqual(json_body['error'], 'key or val too long', msg='Bad error message (put oversized value)')


  # Get non-existent key
  def test_get_nonexistent(self):
    res = get(keys[0])
    self.assertEqual(res.status_code, 404, msg='Did not return status 404 (get non-existent key)')
    json_body = res.json() # Exception if not parsable to json
    self.assertIn('error', json_body, msg='Key "error" not in json response (get non-existent key)')
    self.assertEqual(json_body['error'], 'not found', msg='Bad error message (get non-existent key)')


  # Delete non-existent key
  def test_delete_nonexistent(self):
    res = delete(keys[0])
    self.assertEqual(res.status_code, 404, msg='Did not return status 404 (delete non-existent key)')
    json_body = res.json() # Exception if not parsable to json
    self.assertIn('error', json_body, msg='Key "error" not in json response (delete non-existent key)')
    self.assertEqual(json_body['error'], 'not found', msg='Bad error message (delete non-existent key)')


  # Simple put then get
  def test_put_get(self):
    res = put(keys[0], vals[0])
    self.assertEqual(res.status_code, 201, msg='Did not return status 201 (simple put then get: put)')
    json_body = res.json() # Exception if not parsable to json
    self.assertIn('replaced', json_body, msg='Key "replaced" not in json response (simple put then get: put)')
    self.assertEqual(json_body['replaced'], False, msg='Bad value for key "replaced" (simple put then get: put)')

    res = get(keys[0])
    self.assertEqual(res.status_code, 200, msg='Did not return status 200 (simple put then get: get)')
    json_body = res.json() # Exception if not parsable to json
    self.assertIn('val', json_body, msg='Key "val" not in json response (simple put then get: get)')
    self.assertEqual(json_body['val'], vals[0], msg='Bad value for key "val" (simple put then get: get)')


  # put, replace, get
  def test_put_replace_get(self):
    put(keys[0], vals[0])

    res = put(keys[0], vals[1])
    self.assertEqual(res.status_code, 200, msg='Did not return status 200 (put-replace-get: replace)')
    json_body = res.json() # Exception if not parsable to json
    self.assertIn('replaced', json_body, msg='Key "replaced" not in json response (put-replace-get: replace)')
    self.assertEqual(json_body['replaced'], True, msg='Bad value for key "replaced" (put-replace-get: replace)')
    self.assertIn('prev', json_body, msg='Key "prev" not in json response (put-replace-get: replace)')
    self.assertEqual(json_body['prev'], vals[0], msg='Bad value for key "prev" (put-replace-get: replace)')

    res = get(keys[0])
    self.assertEqual(res.status_code, 200, msg='Did not return status 200 (put-replace-get: get)')
    json_body = res.json() # Exception if not parsable to json
    self.assertIn('val', json_body, msg='Key "val" not in json response (put-replace-get: get)')
    self.assertEqual(json_body['val'], vals[1], msg='Bad value for key "val" (put-replace-get: get)')


  # put, delete, get
  def test_put_delete_get(self):
    put(keys[0], vals[0])

    res = delete(keys[0])
    self.assertEqual(res.status_code, 200, msg='Did not return status 200 (put-delete-get: delete)')
    json_body = res.json() # Exception if not parsable to json
    self.assertIn('prev', json_body, msg='Key "prev" not in json response (put-delete-get: delete)')
    self.assertEqual(json_body['prev'], vals[0], msg='Bad value for key "prev" (put-delete-get: delete)')

    res = get(keys[0])
    self.assertEqual(res.status_code, 404, msg='Did not return status 404 (put-delete-get: get)')
    json_body = res.json() # Exception if not parsable to json
    self.assertIn('error', json_body, msg='Key "error" not in json response (put-delete-get: get)')
    self.assertEqual(json_body['error'], 'not found', msg='Bad error message (put-delete-get: get)')


  # Multiple key-values
  def test_multiple_kvs(self):
    put(keys[0], vals[0])
    put(keys[1], vals[1])
    res = get(keys[0])
    self.assertEqual(res.json()['val'], vals[0], 'Bad value for key 0 (multiple key-values)')
    res = get(keys[1])
    self.assertEqual(res.json()['val'], vals[1], 'Bad value for key 1 (multiple key-values)')


if __name__ == '__main__':
  unittest.main()
