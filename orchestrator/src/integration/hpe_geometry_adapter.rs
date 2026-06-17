use std::sync::Arc;
use crate::geometry::CausalGeometryService;
use crate::integration::hpe_data_fabric::HpeDataFabricExporter;

pub struct HpeGeometryAdapter {
    geometry: Arc<CausalGeometryService>,
    exporter: Arc<HpeDataFabricExporter>,
}

impl HpeGeometryAdapter {
    pub fn new(geometry: Arc<CausalGeometryService>, exporter: Arc<HpeDataFabricExporter>) -> Self {
        Self { geometry, exporter }
    }

    pub async fn push_geometry_metrics(&self) -> Result<(), String> {
        let metrics = serde_json::json!({
            "timestamp": chrono::Utc::now().to_rfc3339(),
            "concept_count": self.geometry.get_concept_count().await,
            "avg_orthogonality": self.geometry.avg_orthogonality().await,
            "steering_vectors_active": self.geometry.active_steering_count().await,
            "causal_rank_avg": self.geometry.causal_rank_avg().await,
        });

        self.exporter.push_geometry_metrics(metrics).await
    }
}
