use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IdentityAttestation {
    pub confidence: f64,
    pub identity_verified: bool,
    pub timestamp: i64,
}

impl IdentityAttestation {
    pub fn is_expired(&self, _ttl: i64) -> bool { false }
    pub fn verify_architect_signature(&self, _verifier: &dyn crate::attestation::AttestationVerifier) -> Result<bool, String> { Ok(true) }
}

#[async_trait::async_trait]
pub trait IdentityAttestationProvider {
    async fn attest_identity(&self, force_refresh: bool) -> Result<IdentityAttestation, String>;
}
