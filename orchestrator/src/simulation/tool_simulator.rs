use std::sync::Arc;
use crate::geometry::CausalGeometryService;
use ndarray::Array1;
use super::runner::{CandidateResponse, ToolResponse};

pub trait LlmClient: Send + Sync {
    fn generate<'a>(&'a self, prompt: &'a str) -> std::pin::Pin<Box<dyn std::future::Future<Output = Result<String, String>> + Send + 'a>>;
}

pub struct ToolSimulator {
    geometry: Arc<CausalGeometryService>,
    llm_client: Arc<dyn LlmClient>,
}

impl ToolSimulator {
    pub async fn simulate_tool_call(
        &self,
        tool_name: &str,
        parameters: &serde_json::Value,
        context_embedding: &Array1<f32>,
        previous_tool_responses: &[ToolResponse],
    ) -> Result<ToolResponse, String> {
        let _causal_context = self.geometry.project_causal(context_embedding);

        let prompt = format!(
            "Given the following context embedding (causal projection), simulate the response for tool '{}' with parameters: {}. Previous responses: {:?}",
            tool_name, parameters, previous_tool_responses.iter().map(|t| &t.tool_name).collect::<Vec<_>>()
        );

        let response = self.llm_client.generate(&prompt).await?;

        let response_emb = self.geometry.embed(&response);
        let orthogonality = self.geometry.causal_orthogonality(&context_embedding.view(), &response_emb.view());
        if orthogonality < 0.6 {
            // Regenerate if too close to context (would indicate unrealistic tool behavior)
        }

        Ok(ToolResponse { tool_name: tool_name.to_string(), response })
    }

    pub async fn simulate_tool_calls(
        &self,
        _candidate_response: &CandidateResponse,
        _context_embedding: &Array1<f32>
    ) -> Result<Vec<ToolResponse>, String> {
        Ok(vec![])
    }
}
