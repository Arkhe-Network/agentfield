pub mod manager;

pub use manager::{AttestationManager, PolicyDescriptor};

// Mocks to make server compile
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExecutionAttestation {}

impl ExecutionAttestation {
    pub fn is_policy_compliant(&self) -> bool { true }
    pub fn policy_attestation_id(&self) -> String { "mock".to_string() }
}

#[async_trait::async_trait]
pub trait AttestationProvider {
    async fn run_authorized(
        &self,
        workload: &str,
        cost_cap: Option<f64>,
        identity: &crate::identity_attestation::IdentityAttestation,
    ) -> Result<ExecutionAttestation, String>;
}

pub trait AttestationVerifier {
}

pub struct CathedralComputeProvider {}

impl CathedralComputeProvider {
    pub fn new(
        _architect_signer: std::sync::Arc<()>,
        _nervous_system: std::sync::Arc<()>,
        _event_store: std::sync::Arc<()>,
        _version: &str,
    ) -> Self {
        Self {}
    }
}

#[async_trait::async_trait]
impl AttestationProvider for CathedralComputeProvider {
    async fn run_authorized(
        &self,
        _workload: &str,
        _cost_cap: Option<f64>,
        _identity: &crate::identity_attestation::IdentityAttestation,
    ) -> Result<ExecutionAttestation, String> {
        Ok(ExecutionAttestation {})
    }
}
