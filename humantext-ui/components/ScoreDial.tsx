'use client';
import React, { useEffect, useState } from 'react';

interface ScoreDialProps {
  score: number; // 0.0 to 1.0
  label: string;
  color: string;
}

export default function ScoreDial({ score, label, color }: ScoreDialProps) {
  const [animatedScore, setAnimatedScore] = useState(0);
  const radius = 36;
  const circumference = 2 * Math.PI * radius;
  
  useEffect(() => {
    // Animate score from 0 to target
    const target = Math.round(score * 100);
    let current = 0;
    const interval = setInterval(() => {
      current += 2;
      if (current >= target) {
        setAnimatedScore(target);
        clearInterval(interval);
      } else {
        setAnimatedScore(current);
      }
    }, 20);
    return () => clearInterval(interval);
  }, [score]);

  const strokeDashoffset = circumference - (animatedScore / 100) * circumference;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px' }}>
      <div style={{ position: 'relative', width: '80px', height: '80px' }}>
        {/* Background Ring */}
        <svg width="80" height="80" style={{ transform: 'rotate(-90deg)' }}>
          <circle
            cx="40"
            cy="40"
            r={radius}
            stroke="rgba(255, 255, 255, 0.1)"
            strokeWidth="6"
            fill="transparent"
          />
          {/* Progress Ring */}
          <circle
            cx="40"
            cy="40"
            r={radius}
            stroke={color}
            strokeWidth="6"
            fill="transparent"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            style={{ transition: 'stroke-dashoffset 0.1s ease-out' }}
          />
        </svg>
        <div style={{
          position: 'absolute',
          top: 0, left: 0, right: 0, bottom: 0,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontWeight: '600', fontSize: '1.2rem'
        }}>
          {animatedScore}%
        </div>
      </div>
      <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', fontWeight: '500' }}>
        {label}
      </div>
    </div>
  );
}
