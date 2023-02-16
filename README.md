# Qding_backend

랜덤 닉네임 생성

전범위에 쓰이는 댓글을 기능 편의성을 위해 generic foreign key로 시도하였으나
query 효율성이 떨어져 model을 각자 생성하기로 함

save props로 updated_fields 넣으면 auto_now 생략하고 해당 fields만 업데이트 가능