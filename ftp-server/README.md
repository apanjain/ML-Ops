# Setting up the SFTP Server
To setup the SFTP server, we’ve used [Atmoz Docker Image](https://hub.docker.com/r/atmoz/sftp). Following are the steps taken to get it up and running.

## Making a persistent volume
```apiVersion: v1
kind: PersistentVolume
metadata:
  name: data-ftp
spec:
  storageClassName: "mystcls"
  capacity:
    storage: 100Gi
  accessModes:
    - ReadWriteOnce
  claimRef:
    namespace: default
    name: data-claim-ftp
  gcePersistentDisk:
    pdName: ftp-server
    fsType: ext4 
```

Here we’ve taken a storage of size 100Gigs. “claimRef:name:data-claim-ftp” will be used by the Persistent Volume Claim to bind this volume to the cluster.

## Persistent Volume Claim
```apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-claim-ftp
spec:
  storageClassName: "mystcls"
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Gi
```

## Defining the ConfigMap
```apiVersion: v1
kind: ConfigMap
metadata:
  name: ftp-configmap
data:
  # property-like keys; each key maps to a simple value
  users.conf: |
    mk1:demo:1020:100:/uploads
    mk2:demo:1021:100:/uploads
    mk3:demo:1022:100:/uploads
```

- Here “mk1, mk2 and mk3” are the defined user names for different accounts on the same server and “demo” as their password. 
- “1020”, “1021” and “1022” are the User IDs and “100” is the group ID. 
- “/uploads” is the directory in which users will upload their data. 

## Creating the Deployment and the corresponding Service
```apiVersion: apps/v1
kind: Deployment
metadata:
  name: ftp-d0
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ftpd0
  template:
    metadata:
      labels:
        app: ftpd0
    spec:
      containers:
        - name: ftp-c
          image: atmoz/sftp
          ports:
            - containerPort: 22
          volumeMounts:
            - mountPath: "/etc/sftp"
              name: config
              readOnly: true
            - mountPath: "/home/"
              name: data-ftp
            - mountPath: "/etc/ssh/ssh_host_ed25519_key"
              name: data-ftp
              subPath: "ssh-keys/ssh_host_ed25519_key"
            - mountPath: "/etc/ssh/ssh_host_rsa_key"
              name: data-ftp
              subPath: "ssh-keys/ssh_host_rsa_key"
      volumes:
        - name: config
          configMap:
            name: ftp-configmap
            items:
              - key: "users.conf"
                path: "users.conf"
        - name: data-ftp
          persistentVolumeClaim:
            claimName: data-claim-ftp
---
apiVersion: v1
kind: Service
metadata:
  name: ftp-service
  labels:
    name: ftp-app
spec:
  ports:
    - port: 22
      name: ftp-port
      protocol: TCP
  selector:
    app: ftpd0
  type: LoadBalancer
```

We provided custom generated keys using:
```ssh-keygen -t ed25519 -f ssh_host_ed25519_key < /dev/null
ssh-keygen -t rsa -b 4096 -f ssh_host_rsa_key < /dev/null
```

Once generated, these can be mounted via the following container
```docker run \
    -v <host-dir>/ssh_host_ed25519_key:/etc/ssh/ssh_host_ed25519_key \
    -v <host-dir>/ssh_host_rsa_key:/etc/ssh/ssh_host_rsa_key \
    -v <host-dir>/share:/home/foo/share \
    -p 2222:22 -d atmoz/sftp \
    foo::1001
```

## References
- https://cloudlets.io/en/kubernetes-blog/setting-up-ftp-server-in-kubernetes/
- https://github.com/atmoz/sftp
