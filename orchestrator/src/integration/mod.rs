pub mod hpe_simulation_adapter;
pub mod hpe_geometry_adapter;

pub use hpe_simulation_adapter::*;
pub use hpe_geometry_adapter::*;

pub mod hpe_data_fabric {
    pub struct HpeDataFabricExporter {}
    impl HpeDataFabricExporter {
        pub async fn push_geometry_metrics(&self, _metrics: serde_json::Value) -> Result<(), String> {
            Ok(())
        }
        pub async fn push_simulation_metrics(&self, _metrics: serde_json::Value) -> Result<(), String> {
            Ok(())
        }
    }
}
