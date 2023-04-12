import os
import httpx
import time

def get_device_serial():
  serial = None
  # string to search in file
  try:
    with open(r'/home/setup/fedge-variables.env', 'r') as fp:
      lines = fp.readlines()
      for row in lines:
        if row.find("SERIAL_NUMBER") != -1:
          serial = row.split("=")[-1]
  except Exception as e:
    print(f"Error occured: {e}\nCannot open env file")
  return serial.replace("\n", "")


def fetch_config(serial_num):
  tenant_id, edge_id, key = None, None, None
  header = {"serial-number": serial_num}
  try:
    res = httpx.get(dev_config_api, headers=header, timeout=None)
    res_json = res.json()
    tenant_id = res_json['data']['X_Tenant_id']
    edge_id = res_json['data']['kcedgedevice_id']
    key = "dckr_pat_W6ZTuEajBNpaL8abWIMOdR-73bc"
  except Exception as e:
    print(f"Error occured: {e}\nAPI failed!")
  return tenant_id, edge_id, key


if __name__ == "__main__":
  with open("/home/setup/fedge-variables.env", "a") as env_file:
    env_file.write(f"TEST_ENV=Ria\n")
  dev_config_api = "https://dev.digitkart.ai/api/frictionless/api/kc/getEdgeDeviceConfig"
  tenant_id, edge_id, key = fetch_config(get_device_serial())
  try:
    with open("/home/setup/fedge-variables.env", "a") as env_file:
      env_file.write(f"TENANT_ID={tenant_id}\n")
      env_file.write(f"EDGE_ID={edge_id}\n")
      env_file.write(f"TOPIC5={tenant_id}/{edge_id}/start-transaction\n")
      env_file.write(f"TOPIC6={tenant_id}/{edge_id}/stop-transaction\n")
      env_file.write(f"TRANSACTION_TOPIC={tenant_id}/{edge_id}/start-transaction")
  except Exception as e:
    print(f"Error occured: {e}\nCannot create env variables.")
  try:
    cmd = f"docker login -u meontechno -p {key}"
    os.system(cmd)
  except Exception as e:
    print(f"Error occured: {e}\nUnable to login to docker...")
