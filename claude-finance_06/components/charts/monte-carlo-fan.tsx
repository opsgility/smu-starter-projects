'use client';

import { ParentSize } from '@visx/responsive';
import { Group } from '@visx/group';
import { AreaClosed, LinePath } from '@visx/shape';
import { scaleLinear } from '@visx/scale';
import { AxisBottom, AxisLeft } from '@visx/axis';
import { GridRows } from '@visx/grid';
import { curveMonotoneX } from '@visx/curve';
import { useTooltip, TooltipWithBounds, defaultStyles } from '@visx/tooltip';
import { localPoint } from '@visx/event';
import { formatCurrency, formatCurrencyAbbrev } from '@/lib/utils/format';
import type { MonteCarloResult } from '@/lib/finance/monte-carlo';

const margin = { top: 20, right: 30, bottom: 40, left: 70 };

interface BandPoint {
  age: number;
  lo: number;
  hi: number;
}

interface MedianPoint {
  age: number;
  v: number;
}

interface TooltipDatum {
  year: number;
  age: number;
  p10: number;
  p50: number;
  p90: number;
}

function FanChartInner({
  width,
  height,
  result,
  startAge,
}: {
  width: number;
  height: number;
  result: MonteCarloResult;
  startAge: number;
}) {
  const inner = {
    width: width - margin.left - margin.right,
    height: height - margin.top - margin.bottom,
  };
  const years = result.percentiles.p50.length;
  const xData = Array.from({ length: years }, (_, i) => startAge + i);

  const x = scaleLinear<number>({
    domain: [startAge, startAge + years - 1],
    range: [0, inner.width],
  });
  const yMax = Math.max(...result.percentiles.p90, 1);
  const y = scaleLinear<number>({
    domain: [0, yMax],
    range: [inner.height, 0],
    nice: true,
  });

  const outerBand: BandPoint[] = xData.map((age, i) => ({
    age,
    lo: result.percentiles.p10[i],
    hi: result.percentiles.p90[i],
  }));
  const innerBand: BandPoint[] = xData.map((age, i) => ({
    age,
    lo: result.percentiles.p25[i],
    hi: result.percentiles.p75[i],
  }));
  const median: MedianPoint[] = xData.map((age, i) => ({
    age,
    v: result.percentiles.p50[i],
  }));

  const {
    tooltipOpen,
    tooltipLeft,
    tooltipTop,
    tooltipData,
    showTooltip,
    hideTooltip,
  } = useTooltip<TooltipDatum>();

  const handleMouseMove = (event: React.MouseEvent<SVGRectElement>) => {
    const point = localPoint(event);
    if (!point) return;
    // Convert from the overlay's coordinate space back to the data x value.
    const xValue = x.invert(point.x - margin.left);
    let idx = Math.round(xValue - startAge);
    if (idx < 0) idx = 0;
    if (idx > years - 1) idx = years - 1;

    const datum: TooltipDatum = {
      year: idx,
      age: startAge + idx,
      p10: result.percentiles.p10[idx],
      p50: result.percentiles.p50[idx],
      p90: result.percentiles.p90[idx],
    };

    showTooltip({
      tooltipData: datum,
      tooltipLeft: margin.left + x(datum.age),
      tooltipTop: margin.top + y(datum.p50),
    });
  };

  return (
    <>
      <svg width={width} height={height}>
        <Group left={margin.left} top={margin.top}>
          <GridRows scale={y} width={inner.width} stroke="rgb(255 255 255 / 0.05)" />

          <AreaClosed<BandPoint>
            data={outerBand}
            x={(d) => x(d.age)}
            y0={(d) => y(d.lo)}
            y1={(d) => y(d.hi)}
            yScale={y}
            fill="oklch(0.62 0.18 264 / 0.15)"
            curve={curveMonotoneX}
          />
          <AreaClosed<BandPoint>
            data={innerBand}
            x={(d) => x(d.age)}
            y0={(d) => y(d.lo)}
            y1={(d) => y(d.hi)}
            yScale={y}
            fill="oklch(0.62 0.18 264 / 0.35)"
            curve={curveMonotoneX}
          />

          <LinePath<MedianPoint>
            data={median}
            x={(d) => x(d.age)}
            y={(d) => y(d.v)}
            stroke="oklch(0.78 0.16 162)"
            strokeWidth={2.5}
            curve={curveMonotoneX}
          />

          <AxisBottom
            scale={x}
            top={inner.height}
            tickFormat={(n) => `Age ${n}`}
            stroke="rgb(255 255 255 / 0.2)"
            tickStroke="rgb(255 255 255 / 0.2)"
            tickLabelProps={() => ({
              fill: 'rgb(255 255 255 / 0.6)',
              fontSize: 11,
              textAnchor: 'middle',
            })}
          />
          <AxisLeft
            scale={y}
            tickFormat={(v) => formatCurrencyAbbrev(v as number)}
            stroke="rgb(255 255 255 / 0.2)"
            tickStroke="rgb(255 255 255 / 0.2)"
            tickLabelProps={() => ({
              fill: 'rgb(255 255 255 / 0.6)',
              fontSize: 11,
              textAnchor: 'end',
              dx: '-0.25em',
            })}
          />

          {tooltipOpen && tooltipData && (
            <g pointerEvents="none">
              <line
                x1={x(tooltipData.age)}
                x2={x(tooltipData.age)}
                y1={0}
                y2={inner.height}
                stroke="rgb(255 255 255 / 0.3)"
                strokeDasharray="3,3"
              />
              <circle
                cx={x(tooltipData.age)}
                cy={y(tooltipData.p50)}
                r={4}
                fill="oklch(0.78 0.16 162)"
                stroke="rgb(0 0 0 / 0.6)"
                strokeWidth={1}
              />
            </g>
          )}

          {/* Transparent overlay captures mouse events across the plot area. */}
          <rect
            x={0}
            y={0}
            width={inner.width}
            height={inner.height}
            fill="transparent"
            onMouseMove={handleMouseMove}
            onMouseLeave={hideTooltip}
          />
        </Group>
      </svg>

      {tooltipOpen && tooltipData && (
        <TooltipWithBounds
          top={tooltipTop}
          left={tooltipLeft}
          style={{
            ...defaultStyles,
            background: 'var(--color-rs-card)',
            border: '1px solid var(--color-rs-border)',
            color: 'var(--color-rs-fg)',
            padding: '8px 10px',
            borderRadius: 8,
            fontSize: 12,
            lineHeight: 1.4,
            boxShadow: '0 4px 12px rgb(0 0 0 / 0.4)',
          }}
        >
          <div
            style={{
              fontWeight: 600,
              marginBottom: 4,
              color: 'var(--color-rs-fg)',
            }}
          >
            Year {tooltipData.year} · Age {tooltipData.age}
          </div>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'auto auto',
              columnGap: 12,
              rowGap: 2,
              fontFamily:
                'ui-monospace, SFMono-Regular, Menlo, monospace',
              fontVariantNumeric: 'tabular-nums',
            }}
          >
            <span style={{ color: 'var(--color-rs-fg-muted)' }}>p90</span>
            <span style={{ textAlign: 'right' }}>
              {formatCurrency(tooltipData.p90)}
            </span>
            <span style={{ color: 'var(--color-rs-fg-muted)' }}>p50</span>
            <span style={{ textAlign: 'right' }}>
              {formatCurrency(tooltipData.p50)}
            </span>
            <span style={{ color: 'var(--color-rs-fg-muted)' }}>p10</span>
            <span style={{ textAlign: 'right' }}>
              {formatCurrency(tooltipData.p10)}
            </span>
          </div>
        </TooltipWithBounds>
      )}
    </>
  );
}

export function MonteCarloFan({
  result,
  startAge,
}: {
  result: MonteCarloResult;
  startAge: number;
}) {
  return (
    <div className="relative h-96 bg-rs-surface border border-rs-border rounded-2xl p-4">
      <ParentSize>
        {({ width, height }: { width: number; height: number }) => (
          <FanChartInner
            width={width}
            height={height}
            result={result}
            startAge={startAge}
          />
        )}
      </ParentSize>
    </div>
  );
}
