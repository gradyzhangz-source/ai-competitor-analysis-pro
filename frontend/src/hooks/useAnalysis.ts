import { useReducer, useCallback } from 'react';
import { AnalysisRequest, AnalysisState, ProgressEvent } from '../types';
import { startAnalysisStream } from '../api/client';

interface AnalysisHookState {
  isRunning: boolean;
  progress: ProgressEvent[];
  result: AnalysisState | null;
  error: string | null;
}

type Action =
  | { type: 'START' }
  | { type: 'PROGRESS'; payload: ProgressEvent }
  | { type: 'RESULT'; payload: AnalysisState }
  | { type: 'ERROR'; payload: string };

function reducer(state: AnalysisHookState, action: Action): AnalysisHookState {
  switch (action.type) {
    case 'START':
      return { isRunning: true, progress: [], result: null, error: null };
    case 'PROGRESS': {
      const newProgress = [...state.progress];
      newProgress[action.payload.stage_idx] = action.payload;
      return { ...state, progress: newProgress };
    }
    case 'RESULT':
      return { ...state, isRunning: false, result: action.payload };
    case 'ERROR':
      return { ...state, isRunning: false, error: action.payload };
    default:
      return state;
  }
}

export function useAnalysis() {
  const [state, dispatch] = useReducer(reducer, {
    isRunning: false,
    progress: [],
    result: null,
    error: null,
  });

  const startAnalysis = useCallback(async (request: AnalysisRequest) => {
    dispatch({ type: 'START' });
    await startAnalysisStream(
      request,
      (data) => dispatch({ type: 'PROGRESS', payload: data }),
      (data) => dispatch({ type: 'RESULT', payload: data }),
      (err) => dispatch({ type: 'ERROR', payload: err?.message || String(err) })
    );
  }, []);

  return { ...state, startAnalysis };
}
