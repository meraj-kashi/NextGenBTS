storage "raft" {
     path = "/vault/raft"
     node_id = "vault_1"
}
listener "tcp" {
     address     = "0.0.0.0:8200"
     cluster_address     = "0.0.0.0:8201"
     tls_disable = true
     telemetry {
        unauthenticated_metrics_access = true
        }      
}

disable_mlock = true
ui=true
telemetry {
  disable_hostname = true
  prometheus_retention_time = "12h"
}
