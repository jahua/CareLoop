"use client";

import type { PipelineMeta } from "./types";

type PipelineInfoProps = {
  pipeline: PipelineMeta;
};

export default function PipelineInfo({ pipeline }: PipelineInfoProps) {
  const hasTimings = pipeline.stage_timings && pipeline.stage_timings.length > 0;
  const hasStatus = pipeline.pipeline_status && Object.keys(pipeline.pipeline_status).length > 0;

  if (!hasTimings && !hasStatus && !pipeline.mode_confidence && !pipeline.mode_routing_reason) {
    return null;
  }

  return (
    <details className="careloop-pipeline">
      <summary className="careloop-pipeline__summary">
        Pipeline
        {pipeline.mode_confidence != null && (
          <span className="careloop-pipeline__conf">
            {Math.round(pipeline.mode_confidence * 100)}% conf
          </span>
        )}
      </summary>
      <div className="careloop-pipeline__body">
        {pipeline.mode_routing_reason && (
          <div className="careloop-pipeline__row">
            <span className="careloop-pipeline__key">Routing</span>
            <span className="careloop-pipeline__val">
              {pipeline.mode_routing_reason.replace(/_/g, " ")}
            </span>
          </div>
        )}
        {hasStatus && (
          <div className="careloop-pipeline__stages">
            {Object.entries(pipeline.pipeline_status!).map(([stage, status]) => (
              <span
                key={stage}
                className={`careloop-pipeline__stage careloop-pipeline__stage--${status}`}
                title={`${stage}: ${status}`}
              >
                {stage}
              </span>
            ))}
          </div>
        )}
        {hasTimings && (
          <div className="careloop-pipeline__timings">
            {pipeline.stage_timings!.map((t) => (
              <div key={t.stage} className="careloop-pipeline__row">
                <span className="careloop-pipeline__key">{t.stage}</span>
                <span className="careloop-pipeline__val">{t.ms}ms</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </details>
  );
}
