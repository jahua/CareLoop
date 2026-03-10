"use client";

import type { PipelineMeta } from "./types";

type PipelineInfoProps = {
  pipeline: PipelineMeta;
};

export default function PipelineInfo({ pipeline }: PipelineInfoProps) {
  const hasTimings = pipeline.stage_timings && pipeline.stage_timings.length > 0;
  const hasStatus = pipeline.pipeline_status && Object.keys(pipeline.pipeline_status).length > 0;

  if (
    !hasTimings &&
    !hasStatus &&
    !pipeline.mode_confidence &&
    !pipeline.mode_routing_reason &&
    !pipeline.route_key &&
    !pipeline.isolation_scope
  ) {
    return null;
  }

  return (
    <details className="big5loop-pipeline">
      <summary className="big5loop-pipeline__summary">
        Pipeline
        {pipeline.mode_confidence != null && (
          <span className="big5loop-pipeline__conf">
            {Math.round(pipeline.mode_confidence * 100)}% conf
          </span>
        )}
      </summary>
      <div className="big5loop-pipeline__body">
        {pipeline.mode_routing_reason && (
          <div className="big5loop-pipeline__row">
            <span className="big5loop-pipeline__key">Routing</span>
            <span className="big5loop-pipeline__val">
              {pipeline.mode_routing_reason.replace(/_/g, " ")}
            </span>
          </div>
        )}
        {pipeline.route_key && (
          <div className="big5loop-pipeline__row">
            <span className="big5loop-pipeline__key">Route key</span>
            <span className="big5loop-pipeline__val">{pipeline.route_key}</span>
          </div>
        )}
        {pipeline.isolation_scope && (
          <div className="big5loop-pipeline__row">
            <span className="big5loop-pipeline__key">Isolation</span>
            <span className="big5loop-pipeline__val">{pipeline.isolation_scope.replace(/_/g, " ")}</span>
          </div>
        )}
        {typeof pipeline.history_turns_used === "number" && (
          <div className="big5loop-pipeline__row">
            <span className="big5loop-pipeline__key">History used</span>
            <span className="big5loop-pipeline__val">
              {pipeline.history_turns_used}
              {pipeline.history_filtered ? " isolated" : " shared"}
            </span>
          </div>
        )}
        {hasStatus && (
          <div className="big5loop-pipeline__stages">
            {Object.entries(pipeline.pipeline_status!).map(([stage, status]) => (
              <span
                key={stage}
                className={`big5loop-pipeline__stage big5loop-pipeline__stage--${status}`}
                title={`${stage}: ${status}`}
              >
                {stage}
              </span>
            ))}
          </div>
        )}
        {hasTimings && (
          <div className="big5loop-pipeline__timings">
            {pipeline.stage_timings!.map((t) => (
              <div key={t.stage} className="big5loop-pipeline__row">
                <span className="big5loop-pipeline__key">{t.stage}</span>
                <span className="big5loop-pipeline__val">{t.ms}ms</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </details>
  );
}
