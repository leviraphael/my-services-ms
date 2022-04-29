## Usage

Before az deployment replace the values placeholder with your K8S profile keys (in your output directory)

```bash
                       "windowsProfile":  {
                                              "adminUsername":  <username>,
                                              "adminPassword":  <password>,
                                              "sshEnabled":  true
                                          },
                       "linuxProfile":  {
                                            "adminUsername":  <admin>,
                                            "ssh":  {
                                                        "publicKeys":  [
                                                                           {
                                                                               "keyData":  <key>
                                                                           }
                                                                       ]
                                                    }
                                        },
                       "servicePrincipalProfile":  {
                                                       "clientId":  <client_id>,
                                                       "secret":  <secret>
```

