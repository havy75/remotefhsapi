from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class Performance(BaseModel):
    eval_year_month: date
    employee_id: str
    employee_name: str
    grade: str
    nationality: str
    dept_code: str
    dept_name: str
    rank_code6: str
    rank_name: str
    first_score: str
    first_comment: str
    first_supervisor: str
    review_score: str
    review_comment: str
    review_supervisor: str
    final_score: str
    final_comment: str
    final_supervisor: str
    mgr_first_score: str
    mgr_first_comment: str
    mgr_first_supervisor: str
    mgr_review_score: str
    mgr_review_comment: str
    mgr_review_supervisor: str
    mgr_final_score: str
    mgr_final_comment: str
    mgr_final_supervisor: str
    leave_days_total: int
    id: Optional[int] = None

class DormUtility(BaseModel):
    period_month: date
    dorm_no: str
    employee_id: str
    employee_name: str
    elec_prev_read: int
    elec_curr_read: int
    elec_usage: int
    elec_amount: int
    water_prev_read: int
    water_curr_read: int
    water_usage: int
    water_amount: int
    shared_fee: int
    cleaning_fee: int
    total_amount: int
    id: Optional[int] = None
