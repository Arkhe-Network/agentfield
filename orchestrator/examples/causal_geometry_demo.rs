use cathedral_arkhe::geometry::CausalGeometryService;
use cathedral_arkhe::geometry::embedding_bridge::SimpleEmbedder;
use cathedral_arkhe::geometry::embedding_bridge::EmbeddingModel;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt::init();

    let embedder = std::sync::Arc::new(SimpleEmbedder::new(768));
    let geometry = std::sync::Arc::new(CausalGeometryService::new(embedder.clone(), 768));

    let code_emb = embedder.embed("def fibonacci(n): return n if n < 2 else ...");
    let non_code_emb = embedder.embed("The quick brown fox...");
    let safe_emb = embedder.embed("safe secure code");
    let unsafe_emb = embedder.embed("unsafe insecure code");
    let mem_emb = embedder.embed("memory efficient code");
    let non_mem_emb = embedder.embed("memory inefficient code");

    geometry.register_concept("code", &[code_emb], &[non_code_emb]).await?;
    geometry.register_concept("safety", &[safe_emb], &[unsafe_emb]).await?;
    geometry.register_concept("memory", &[mem_emb], &[non_mem_emb]).await?;

    let _steering = geometry.get_steering_vector("memory_efficient", 0.5).await?;

    let orth = geometry.concept_orthogonality("code", "safety").await.unwrap();
    println!("Ortogonalidade code-safety: {:.3}", orth);

    let policy_engine = cathedral_arkhe::governance::GeometricPolicyEngine::new(geometry.clone());
    let result = policy_engine.authorize(
        cathedral_arkhe::orchestrator::AgentRole::Specialist,
        "generate_kernel",
        "cuda_kernel_code",
        None,
        None,
    ).await;

    match result {
        Ok(()) => println!("✅ Ação autorizada"),
        Err(e) => println!("❌ Ação rejeitada: {}", e),
    }

    Ok(())
}
