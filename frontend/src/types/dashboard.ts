export interface DashboardReportingPeriod {
  mode: 'all_retained' | 'custom'
  startDate: string | null
  endDate: string | null
  timezone: 'Asia/Shanghai'
}

export interface DashboardAggregate {
  reportingPeriod: DashboardReportingPeriod
  updatedAt: string | null
  contactConversion: {
    rate: number | null
    numerator: number
    denominator: number
  }
  eventTotals: {
    pageVisits: number
    jobDescriptionSubmissions: number
    matchingReportsGenerated: number
    resumePreviews: number
    contactCtaClicks: number
    feedbackSubmissions: number
  }
}

export interface DashboardDateRange {
  startDate: string
  endDate: string
}

export interface DashboardClient {
  getAggregate(dateRange?: DashboardDateRange): Promise<DashboardAggregate>
}
