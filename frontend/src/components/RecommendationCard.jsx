function RecommendationCard({ analysis }) {
  return (
    <div className="card analysis-panel">
      <strong>Wellness summary</strong>
      <div>
        <span className="status-label">Emotion</span> {analysis.emotion}
      </div>
      <div>
        <span className="status-label">Stress score</span> {analysis.stressScore} / 10
      </div>
      <div>
        <span className="status-label">Recommendation</span>
        <p style={{ marginTop: '10px' }}>{analysis.recommendation}</p>
      </div>
    </div>
  );
}

export default RecommendationCard;
