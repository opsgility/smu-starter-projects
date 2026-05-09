'use client';

import { ParentSize } from '@visx/responsive';
import { Group } from '@visx/group';
import { AreaClosed, LinePath } from '@visx/shape';
import { scaleLinear } from '@visx/scale';
import { AxisBottom, AxisLeft } from '@visx/axis';
import { GridRows } from '@visx/grid';
import { curveMonotoneX } from '@visx/curve';
import { formatCurrencyAbbrev } from '@/lib/utils/format';
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

  return (
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
      </Group>
    </svg>
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
    <div className="h-96 bg-rs-surface border border-rs-border rounded-2xl p-4">
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
