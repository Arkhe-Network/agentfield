use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VoiceEvidence {}

pub struct VoiceCore {}

impl VoiceCore {
    pub async fn capture_phrase_for_proof_of_life(&self, _phrase: Option<&str>) -> Result<VoiceEvidence, String> {
        Ok(VoiceEvidence {})
    }
}
