-- ============================================================
-- 学生宿舍管理系统 MySQL 建表脚本
-- 数据库版本: MySQL 8.0
-- 编码: utf8mb4
-- 说明: Django ORM 会自动建表，本脚本供手动初始化或参考使用
-- ============================================================

CREATE DATABASE IF NOT EXISTS dormitory_db
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE dormitory_db;

-- -----------------------------------------------------------
-- 1. 用户表 (由 Django auth 扩展)
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS sys_user (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    password        VARCHAR(128) NOT NULL,
    last_login      DATETIME(6)  NULL,
    is_superuser    TINYINT(1)   NOT NULL DEFAULT 0,
    username        VARCHAR(150) NOT NULL UNIQUE,
    first_name      VARCHAR(150) NOT NULL DEFAULT '',
    last_name       VARCHAR(150) NOT NULL DEFAULT '',
    email           VARCHAR(254) NOT NULL DEFAULT '',
    is_staff        TINYINT(1)   NOT NULL DEFAULT 0,
    is_active       TINYINT(1)   NOT NULL DEFAULT 1,
    date_joined     DATETIME(6)  NOT NULL,
    role            VARCHAR(10)  NOT NULL DEFAULT 'student'
                    COMMENT '角色: admin=超级管理员, manager=宿管, student=学生',
    phone           VARCHAR(11)  NOT NULL DEFAULT '',
    avatar          VARCHAR(100) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------
-- 2. 楼栋表
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS dorm_building (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(50)  NOT NULL UNIQUE,
    code            VARCHAR(10)  NOT NULL UNIQUE COMMENT '编号, 如 A1',
    floors          INT          NOT NULL DEFAULT 6,
    gender_type     VARCHAR(10)  NOT NULL DEFAULT 'male'
                    COMMENT 'male=男生楼 female=女生楼 mixed=混合楼',
    address         VARCHAR(200) NOT NULL DEFAULT '',
    manager_id      BIGINT       NULL COMMENT '宿管用户ID',
    description     TEXT,
    is_active       TINYINT(1)   NOT NULL DEFAULT 1,
    created_at      DATETIME(6)  NOT NULL,
    updated_at      DATETIME(6)  NOT NULL,
    FOREIGN KEY (manager_id) REFERENCES sys_user(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------
-- 3. 房间表
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS dorm_room (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    building_id     BIGINT       NOT NULL,
    room_number     VARCHAR(20)  NOT NULL,
    room_type       VARCHAR(10)  NOT NULL DEFAULT '四人寝',
    bed_count       INT          NOT NULL DEFAULT 4,
    floor           INT          NOT NULL,
    is_active       TINYINT(1)   NOT NULL DEFAULT 1,
    remark          VARCHAR(200) NOT NULL DEFAULT '',
    UNIQUE KEY uk_building_room (building_id, room_number),
    FOREIGN KEY (building_id) REFERENCES dorm_building(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------
-- 4. 床位表
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS dorm_bed (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    room_id         BIGINT       NOT NULL,
    bed_number      VARCHAR(10)  NOT NULL COMMENT '如 1号床, A床',
    status          VARCHAR(10)  NOT NULL DEFAULT '空闲'
                    COMMENT '空闲/已入住/维修中',
    UNIQUE KEY uk_room_bed (room_id, bed_number),
    FOREIGN KEY (room_id) REFERENCES dorm_room(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------
-- 5. 学生表
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS stu_student (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id         BIGINT       NULL COMMENT '关联系统账户',
    student_id      VARCHAR(20)  NOT NULL UNIQUE COMMENT '学号',
    real_name       VARCHAR(50)  NOT NULL,
    gender          VARCHAR(4)   NOT NULL,
    class_name      VARCHAR(100) NOT NULL DEFAULT '',
    college         VARCHAR(100) NOT NULL DEFAULT '',
    phone           VARCHAR(11)  NOT NULL DEFAULT '',
    parent_phone    VARCHAR(11)  NOT NULL DEFAULT '',
    status          VARCHAR(10)  NOT NULL DEFAULT '在校'
                    COMMENT '在校/毕业/退学/离校',
    enroll_date     DATE         NULL,
    remark          TEXT,
    created_at      DATETIME(6)  NOT NULL,
    updated_at      DATETIME(6)  NOT NULL,
    FOREIGN KEY (user_id) REFERENCES sys_user(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------
-- 6. 住宿记录表
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS stu_dormitory_record (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    student_id      BIGINT       NOT NULL,
    bed_id          BIGINT       NOT NULL,
    status          VARCHAR(10)  NOT NULL DEFAULT '入住中'
                    COMMENT '入住中/已调宿/已退宿',
    checkin_date    DATETIME(6)  NOT NULL,
    checkout_date   DATETIME(6)  NULL,
    operation_type  VARCHAR(10)  NOT NULL DEFAULT '入住'
                    COMMENT '入住/调宿/退宿',
    operator_id     BIGINT       NULL,
    reason          TEXT,
    FOREIGN KEY (student_id) REFERENCES stu_student(id) ON DELETE CASCADE,
    FOREIGN KEY (bed_id) REFERENCES dorm_bed(id) ON DELETE CASCADE,
    FOREIGN KEY (operator_id) REFERENCES sys_user(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------
-- 7. 报修分类表
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS repair_category (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(50)  NOT NULL UNIQUE,
    sort_order      INT          NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------
-- 8. 报修工单表
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS repair_order (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    order_no        VARCHAR(30)  NOT NULL UNIQUE COMMENT '工单编号',
    title           VARCHAR(200) NOT NULL,
    category_id     BIGINT       NULL,
    building_id     BIGINT       NULL,
    room_id         BIGINT       NULL,
    reporter_id     BIGINT       NOT NULL,
    description     TEXT,
    images          VARCHAR(100) NOT NULL DEFAULT '',
    contact_phone   VARCHAR(11)  NOT NULL DEFAULT '',
    status          VARCHAR(10)  NOT NULL DEFAULT '待处理'
                    COMMENT '待处理/处理中/已完成/已关闭',
    assignee_id     BIGINT       NULL,
    handler_note    TEXT,
    created_at      DATETIME(6)  NOT NULL,
    updated_at      DATETIME(6)  NOT NULL,
    completed_at    DATETIME(6)  NULL,
    FOREIGN KEY (category_id) REFERENCES repair_category(id) ON DELETE SET NULL,
    FOREIGN KEY (building_id) REFERENCES dorm_building(id) ON DELETE SET NULL,
    FOREIGN KEY (room_id) REFERENCES dorm_room(id) ON DELETE SET NULL,
    FOREIGN KEY (reporter_id) REFERENCES sys_user(id) ON DELETE CASCADE,
    FOREIGN KEY (assignee_id) REFERENCES sys_user(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------
-- 9. 水电账单表
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS util_utility_bill (
    id                  BIGINT AUTO_INCREMENT PRIMARY KEY,
    building_id         BIGINT       NOT NULL,
    room_id             BIGINT       NOT NULL,
    year                INT          NOT NULL,
    month               INT          NOT NULL,
    utility_type        VARCHAR(15)  NOT NULL COMMENT 'electricity=电费 water=水费',
    previous_reading    DECIMAL(10,2) NOT NULL DEFAULT 0,
    current_reading     DECIMAL(10,2) NOT NULL DEFAULT 0,
    usage               DECIMAL(10,2) NOT NULL DEFAULT 0,
    unit_price          DECIMAL(8,4)  NOT NULL DEFAULT 0.5500,
    amount              DECIMAL(10,2) NOT NULL DEFAULT 0,
    status              VARCHAR(10)   NOT NULL DEFAULT '未缴纳'
                        COMMENT '未缴纳/已缴纳/已减免',
    remark              TEXT,
    created_at          DATETIME(6)   NOT NULL,
    updated_at          DATETIME(6)   NOT NULL,
    UNIQUE KEY uk_room_month_type (room_id, year, month, utility_type),
    FOREIGN KEY (building_id) REFERENCES dorm_building(id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES dorm_room(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------
-- 10. 卫生检查表
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS ins_hygiene_inspection (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    building_id     BIGINT       NOT NULL,
    room_id         BIGINT       NOT NULL,
    inspector_id    BIGINT       NOT NULL,
    score           INT          NOT NULL DEFAULT 8 COMMENT '1-10分',
    grade           VARCHAR(10)  NOT NULL DEFAULT '良好'
                    COMMENT '优秀/良好/合格/不合格',
    comment         TEXT,
    images          VARCHAR(100) NOT NULL DEFAULT '',
    check_date      DATE         NOT NULL,
    created_at      DATETIME(6)  NOT NULL,
    FOREIGN KEY (building_id) REFERENCES dorm_building(id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES dorm_room(id) ON DELETE CASCADE,
    FOREIGN KEY (inspector_id) REFERENCES sys_user(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------
-- 11. 公告表
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS announcement (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    title           VARCHAR(200) NOT NULL,
    content         TEXT,
    category        VARCHAR(10)  NOT NULL DEFAULT 'dorm'
                    COMMENT 'system/dorm/repair/other',
    author_id       BIGINT       NOT NULL,
    is_pinned       TINYINT(1)   NOT NULL DEFAULT 0,
    is_active       TINYINT(1)   NOT NULL DEFAULT 1,
    views           INT          NOT NULL DEFAULT 0,
    created_at      DATETIME(6)  NOT NULL,
    updated_at      DATETIME(6)  NOT NULL,
    FOREIGN KEY (author_id) REFERENCES sys_user(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------
-- 12. 操作日志表
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS log_operation (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id         BIGINT       NULL,
    username        VARCHAR(150) NOT NULL DEFAULT '',
    action          VARCHAR(200) NOT NULL,
    module          VARCHAR(50)  NOT NULL DEFAULT '',
    ip_address      VARCHAR(39)  NULL,
    request_method  VARCHAR(10)  NOT NULL DEFAULT '',
    request_path    VARCHAR(500) NOT NULL DEFAULT '',
    detail          TEXT,
    created_at      DATETIME(6)  NOT NULL,
    FOREIGN KEY (user_id) REFERENCES sys_user(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------
-- 初始数据：默认超级管理员
-- -----------------------------------------------------------
-- 密码: admin123 (pbkdf2_sha256 加密)
-- 首次登录后请修改密码
INSERT INTO sys_user (password, is_superuser, username, first_name, last_name, email,
                      is_staff, is_active, date_joined, role, phone, avatar)
VALUES (
    'pbkdf2_sha256\\\',
    1, 'admin', '', '', 'admin@dormitory.com',
    1, 1, NOW(), 'admin', '13800000000', ''
);

-- -----------------------------------------------------------
-- 初始数据：示例报修分类
-- -----------------------------------------------------------
INSERT INTO repair_category (name, sort_order) VALUES
('水暖维修', 1),
('电力维修', 2),
('门窗维修', 3),
('空调维修', 4),
('网络故障', 5),
('其他', 6);

-- -----------------------------------------------------------
-- 索引建议
-- -----------------------------------------------------------
CREATE INDEX idx_dorm_room_building ON dorm_room(building_id);
CREATE INDEX idx_dorm_room_floor ON dorm_room(floor);
CREATE INDEX idx_dorm_bed_room ON dorm_bed(room_id);
CREATE INDEX idx_stu_record_student ON stu_dormitory_record(student_id);
CREATE INDEX idx_stu_record_status ON stu_dormitory_record(status);
CREATE INDEX idx_repair_status ON repair_order(status);
CREATE INDEX idx_repair_reporter ON repair_order(reporter_id);
CREATE INDEX idx_utility_room_month ON util_utility_bill(room_id, year, month);
CREATE INDEX idx_inspection_date ON ins_hygiene_inspection(check_date);
CREATE INDEX idx_log_user ON log_operation(user_id);
CREATE INDEX idx_log_time ON log_operation(created_at);
