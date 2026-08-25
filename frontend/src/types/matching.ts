export type EvidenceStatus = 'supported' | 'partial' | 'missing'

export type RequirementImportance = 'core' | 'important' | 'additional'

export interface MatchingRequirement {
  id: string
  requirement: string
  importance: RequirementImportance
  status: EvidenceStatus
  finding: string
  evidence: string[]
  informationGap?: string
}

export interface MatchingReport {
  title: string
  requirements: MatchingRequirement[]
  limitations: string[]
}

export interface AnalysisClient {
  analyze(jobDescription: string): Promise<MatchingReport>
}
