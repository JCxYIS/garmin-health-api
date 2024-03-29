# API
API_HOST = 'https://apis.garmin.com'

API_GET_USERID = 'wellness-api/rest/user/id'

# HEALTH API (Restful)
API_DAILY_SUMMARIES = 'wellness-api/rest/dailies'  # 7.1. 每日摘要（Daily Summaries）
API_THIRD_PARTY_DAILY_SUMMARIES = 'wellness-api/rest/thirdPartyDailies'  # 7.2. 第三方每日摘要（Third-Party Daily Summaries）
API_EPOCH_SUMMARIES = 'wellness-api/rest/epochs'  # 7.3. 时期摘要（Epoch Summaries）
API_SLEEP_SUMMARIES = 'wellness-api/rest/sleeps'  # 7.4. 睡眠摘要（Sleep Summaries）
API_COMPOSITION_SUMMARIES = 'wellness-api/rest/bodyComps'  # 7.5. 身体成分摘要（Body Composition Summaries）
API_STRESS_DETAILS_SUMMARIES = 'wellness-api/rest/stressDetails'  # 7.6. 压力详情摘要（Stress Details Summaries）
API_USER_METRICS_SUMMARIES = 'wellness-api/rest/userMetrics'  # 7.7. 用户生理指标摘要（User Metrics Summaries）
API_PULSE_OX_SUMMARIES = 'wellness-api/rest/pulseOx'  # 7.8. 血氧饱和度摘要（Pulse Ox Summaries）
API_RESPIRATION_SUMMARIES = 'wellness-api/rest/respiration'  # 7.9. 呼吸摘要（Respiration Summaries）
API_HEALTH_SNAPSHOT_SUMMARIES = 'wellness-api/rest/healthSnapshot'  # 7.10. 健康快照摘要（Health Snapshot Summaries）
API_HEART_RATE_VARIABILITY_SUMMARIES = 'wellness-api/rest/hrv'  # 7.11. 心率变异性摘要（Heart Rate Variability (HRV) Summaries）
API_BLOOD_PRESSURE_SUMMARIES = 'wellness-api/rest/bloodPressures'  # 7.12. 血压摘要 (Blood Pressure Summaries)
API_HEALTH_ENDPOINTS = {
    'daily_summaries': API_DAILY_SUMMARIES,
    'third_party_daily_summaries': API_THIRD_PARTY_DAILY_SUMMARIES,
    'epoch_summaries': API_EPOCH_SUMMARIES,
    'sleep_summaries': API_SLEEP_SUMMARIES,
    'composition_summaries': API_COMPOSITION_SUMMARIES,
    'stress_details_summaries': API_STRESS_DETAILS_SUMMARIES,
    'user_metrics_summaries': API_USER_METRICS_SUMMARIES,
    'pulse_ox_summaries': API_PULSE_OX_SUMMARIES,
    'respiration_summaries': API_RESPIRATION_SUMMARIES,
    'health_snapshot_summaries': API_HEALTH_SNAPSHOT_SUMMARIES,
    'heart_rate_variability_summaries': API_HEART_RATE_VARIABILITY_SUMMARIES,
    'blood_pressure_summaries': API_BLOOD_PRESSURE_SUMMARIES,
}