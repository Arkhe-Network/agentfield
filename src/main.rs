use std::sync::Arc;
use tracing::{info, error};

pub mod mcp;
pub mod attestation;
pub mod identity_attestation;
pub mod voice;

use crate::attestation::{AttestationManager, CathedralComputeProvider, AttestationProvider, AttestationVerifier};
use crate::identity_attestation::IdentityAttestationProvider;
use crate::voice::VoiceCore;
use crate::mcp::server::start_mcp_server;

// Mocks to make main compile
struct MockIdentityProvider {}
#[async_trait::async_trait]
impl IdentityAttestationProvider for MockIdentityProvider {
    async fn attest_identity(&self, _force_refresh: bool) -> Result<crate::identity_attestation::IdentityAttestation, String> {
        Ok(crate::identity_attestation::IdentityAttestation {
            confidence: 1.0,
            identity_verified: true,
            timestamp: 0,
        })
    }
}


#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Setup tracing
    tracing_subscriber::fmt::init();

    info!("Starting MCP Server integration...");

    let attestation_manager = Arc::new(AttestationManager {});
    let voice_core = Arc::new(VoiceCore {});

    // Mocks for constructor
    let architect_signer = Arc::new(());
    let nervous_system = Arc::new(());
    let event_store = Arc::new(());

    // 1. Configuração do MCP
    let mcp_enabled = std::env::var("ENABLE_MCP_SERVER")
        .unwrap_or_else(|_| "true".to_string())
        .parse::<bool>()
        .unwrap_or(true);

    if mcp_enabled {
        let mcp_port = std::env::var("MCP_PORT")
            .unwrap_or_else(|_| "3032".to_string())
            .parse::<u16>()
            .unwrap_or(3032);

        let mcp_token = std::env::var("MCP_AUTH_TOKEN").ok();

        // 2. Cria execution provider (CathedralComputeProvider)
        let execution_provider: Arc<dyn AttestationProvider + Send + Sync> =
            Arc::new(CathedralComputeProvider::new(
                architect_signer.clone(),
                nervous_system.clone(),
                event_store.clone(),
                "cathedral-v1",
            ));

        // 3. Verificador (pode ser opcional)
        let architect_verifier: Option<Arc<dyn AttestationVerifier + Send + Sync>> = None; // Mock

        // 4. Inicia o servidor
        let attestation_manager_clone = attestation_manager.clone();
        let identity_provider_clone: Arc<dyn IdentityAttestationProvider + Send + Sync> = Arc::new(MockIdentityProvider {});
        let execution_provider_clone = execution_provider.clone();
        let voice_core_clone = Some(voice_core.clone());

        tokio::spawn(async move {
            if let Err(e) = start_mcp_server(
                attestation_manager_clone,
                identity_provider_clone,
                execution_provider_clone,
                architect_verifier,
                voice_core_clone,
                mcp_port,
                mcp_token,
            )
            .await
            {
                error!("❌ MCP Server falhou: {}", e);
            }
        });

        info!("🧠 MCP Server iniciado na porta {}", mcp_port);

        // Wait indefinitely for mock purposes
        tokio::time::sleep(tokio::time::Duration::from_secs(2)).await;
    }

    Ok(())
}
