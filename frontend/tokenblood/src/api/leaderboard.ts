import type { LeaderboardEntry } from '@/types/leaderboard'

export interface LeaderboardResponse {
  data: LeaderboardEntry[];
}

const MOCK_DATA: LeaderboardEntry[] = [
  { rank: 1, username: 'homomorphism', score: 0.98 },
  { rank: 2, username: 'maxikadze', score: 0.91 },
  { rank: 3, username: 'Zuckerberg', score: 0.78 },
  { rank: 4, username: 'tourist', score: 0.77 },
  { rank: 5, username: 'teapot', score: 0.75 },
  { rank: 6, username: 'llm_monster', score: 0.75 },
  { rank: 7, username: 'killer-bee', score: 0.75 },
  { rank: 8, username: 'ilovetanyasergeeva', score: 0.74 },
  { rank: 9, username: 'meandmyhands', score: 0.71 },
  { rank: 10, username: 'randomnickname', score: 0.64 },
  { rank: 11, username: 'nick_vostrukhin', score: 0.51 },
  { rank: 12, username: 'expresso', score: 0.45 },
  { rank: 13, username: 'dumbest', score: 0.24 }
]

export async function fetchLeaderboard(): Promise<LeaderboardResponse> {
  // Simulate network delay
  await new Promise(resolve => setTimeout(resolve, 500))
  return {
    data: MOCK_DATA,
  }
} 