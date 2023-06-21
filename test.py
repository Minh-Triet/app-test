# with app.app_context():
#     check_ip = select_ip_run()
#     scheduler.add_job(job_start, 'interval', seconds=1000, id='koko', replace_existing=True)
#     if check_ip:
#         for ip in check_ip:
#             if ip == ip_host:
#                 if scheduler.state == 0:
#                     scheduler.start()
#                     jobs1 = scheduler.get_job('Job_1_demo')
#                     jobs2 = scheduler.get_job('Job_2_demo')
#                     if not jobs1 or not jobs2:
#                         scheduler.add_job(walk, 'interval', seconds=20, id='Job_1_demo',
#                                           replace_existing=True)
#                         scheduler.add_job(swim, 'interval', seconds=30, id='Job_2_demo',
#                                           replace_existing=True)
#             else:
#                 create_scheduler()
#     else:
#         create_scheduler()