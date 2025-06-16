/*
 Navicat Premium Dump SQL

 Source Server         : local
 Source Server Type    : PostgreSQL
 Source Server Version : 140017 (140017)
 Source Host           : localhost:5432
 Source Catalog        : muteludb
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 140017 (140017)
 File Encoding         : 65001

 Date: 07/06/2025 14:19:27
*/


-- ----------------------------
-- Type structure for addresstype
-- ----------------------------
DROP TYPE IF EXISTS "public"."addresstype";
CREATE TYPE "public"."addresstype" AS ENUM (
  'SHIPPING',
  'BILLING',
  'BOTH'
);

-- ----------------------------
-- Type structure for agegroup
-- ----------------------------
DROP TYPE IF EXISTS "public"."agegroup";
CREATE TYPE "public"."agegroup" AS ENUM (
  'CHILD',
  'TEEN',
  'ADULT',
  'SENIOR',
  'ALL'
);

-- ----------------------------
-- Type structure for attributetype
-- ----------------------------
DROP TYPE IF EXISTS "public"."attributetype";
CREATE TYPE "public"."attributetype" AS ENUM (
  'TEXT',
  'SELECT',
  'MULTISELECT',
  'BOOLEAN',
  'DATE',
  'NUMBER',
  'COLOR'
);

-- ----------------------------
-- Type structure for calculationmethod
-- ----------------------------
DROP TYPE IF EXISTS "public"."calculationmethod";
CREATE TYPE "public"."calculationmethod" AS ENUM (
  'FIXED',
  'PERCENTAGE',
  'PER_ITEM',
  'PER_WEIGHT',
  'PER_DIMENSION',
  'FORMULA'
);

-- ----------------------------
-- Type structure for calculationtype
-- ----------------------------
DROP TYPE IF EXISTS "public"."calculationtype";
CREATE TYPE "public"."calculationtype" AS ENUM (
  'FLAT_RATE',
  'WEIGHT_BASED',
  'PRICE_BASED',
  'VOLUME_BASED',
  'TABLE_RATE',
  'CUSTOM'
);

-- ----------------------------
-- Type structure for categorylevel
-- ----------------------------
DROP TYPE IF EXISTS "public"."categorylevel";
CREATE TYPE "public"."categorylevel" AS ENUM (
  'LEVEL_1',
  'LEVEL_2',
  'LEVEL_3'
);

-- ----------------------------
-- Type structure for conditiontype
-- ----------------------------
DROP TYPE IF EXISTS "public"."conditiontype";
CREATE TYPE "public"."conditiontype" AS ENUM (
  'WEIGHT',
  'PRICE',
  'QUANTITY',
  'VOLUME',
  'DIMENSION',
  'COMBINED'
);

-- ----------------------------
-- Type structure for couponformat
-- ----------------------------
DROP TYPE IF EXISTS "public"."couponformat";
CREATE TYPE "public"."couponformat" AS ENUM (
  'ALPHANUMERIC',
  'NUMERIC',
  'ALPHABETIC',
  'CUSTOM'
);

-- ----------------------------
-- Type structure for couponstatus
-- ----------------------------
DROP TYPE IF EXISTS "public"."couponstatus";
CREATE TYPE "public"."couponstatus" AS ENUM (
  'ACTIVE',
  'INACTIVE',
  'EXPIRED',
  'USED',
  'CANCELLED'
);

-- ----------------------------
-- Type structure for customercouponstatus
-- ----------------------------
DROP TYPE IF EXISTS "public"."customercouponstatus";
CREATE TYPE "public"."customercouponstatus" AS ENUM (
  'AVAILABLE',
  'USED',
  'EXPIRED',
  'CANCELLED'
);

-- ----------------------------
-- Type structure for customerstatus
-- ----------------------------
DROP TYPE IF EXISTS "public"."customerstatus";
CREATE TYPE "public"."customerstatus" AS ENUM (
  'ACTIVE',
  'INACTIVE',
  'LOCKED',
  'DELETED'
);

-- ----------------------------
-- Type structure for discounttype
-- ----------------------------
DROP TYPE IF EXISTS "public"."discounttype";
CREATE TYPE "public"."discounttype" AS ENUM (
  'PERCENTAGE',
  'FIXED_AMOUNT',
  'FREE_ITEM',
  'FIXED_PRICE'
);

-- ----------------------------
-- Type structure for gatewaystatus
-- ----------------------------
DROP TYPE IF EXISTS "public"."gatewaystatus";
CREATE TYPE "public"."gatewaystatus" AS ENUM (
  'ACTIVE',
  'INACTIVE',
  'TESTING',
  'MAINTENANCE'
);

-- ----------------------------
-- Type structure for gendertype
-- ----------------------------
DROP TYPE IF EXISTS "public"."gendertype";
CREATE TYPE "public"."gendertype" AS ENUM (
  'MALE',
  'FEMALE',
  'UNISEX'
);

-- ----------------------------
-- Type structure for giftwraptype
-- ----------------------------
DROP TYPE IF EXISTS "public"."giftwraptype";
CREATE TYPE "public"."giftwraptype" AS ENUM (
  'STANDARD',
  'PREMIUM',
  'DELUXE',
  'FESTIVE',
  'BIRTHDAY',
  'ANNIVERSARY',
  'CUSTOM'
);

-- ----------------------------
-- Type structure for imagetype
-- ----------------------------
DROP TYPE IF EXISTS "public"."imagetype";
CREATE TYPE "public"."imagetype" AS ENUM (
  'MAIN',
  'GALLERY',
  'DETAIL',
  'BANNER',
  'THUMBNAIL',
  'video'
);

-- ----------------------------
-- Type structure for installmentplanstatus
-- ----------------------------
DROP TYPE IF EXISTS "public"."installmentplanstatus";
CREATE TYPE "public"."installmentplanstatus" AS ENUM (
  'ACTIVE',
  'INACTIVE',
  'PROMOTIONAL'
);

-- ----------------------------
-- Type structure for inventoryoperation
-- ----------------------------
DROP TYPE IF EXISTS "public"."inventoryoperation";
CREATE TYPE "public"."inventoryoperation" AS ENUM (
  'PURCHASE',
  'SALE',
  'RETURN',
  'ADJUSTMENT',
  'DAMAGE',
  'TRANSFER'
);

-- ----------------------------
-- Type structure for issuemethod
-- ----------------------------
DROP TYPE IF EXISTS "public"."issuemethod";
CREATE TYPE "public"."issuemethod" AS ENUM (
  'MANUAL',
  'EMAIL',
  'SMS',
  'AUTOMATIC',
  'SIGNUP',
  'REFERRAL',
  'PURCHASE',
  'LOYALTY',
  'GIVEAWAY'
);

-- ----------------------------
-- Type structure for labelformat
-- ----------------------------
DROP TYPE IF EXISTS "public"."labelformat";
CREATE TYPE "public"."labelformat" AS ENUM (
  'PDF',
  'ZPL',
  'PNG',
  'JPG'
);

-- ----------------------------
-- Type structure for labelstatus
-- ----------------------------
DROP TYPE IF EXISTS "public"."labelstatus";
CREATE TYPE "public"."labelstatus" AS ENUM (
  'PENDING',
  'GENERATED',
  'PRINTED',
  'CANCELLED',
  'ERROR'
);

-- ----------------------------
-- Type structure for materialtype
-- ----------------------------
DROP TYPE IF EXISTS "public"."materialtype";
CREATE TYPE "public"."materialtype" AS ENUM (
  'GEMSTONE',
  'CRYSTAL',
  'WOOD',
  'METAL',
  'FABRIC',
  'CERAMIC',
  'STONE',
  'BAMBOO',
  'OTHER'
);

-- ----------------------------
-- Type structure for membershiplevel
-- ----------------------------
DROP TYPE IF EXISTS "public"."membershiplevel";
CREATE TYPE "public"."membershiplevel" AS ENUM (
  'REGULAR',
  'SILVER',
  'GOLD',
  'PLATINUM',
  'DIAMOND'
);

-- ----------------------------
-- Type structure for occasiontype
-- ----------------------------
DROP TYPE IF EXISTS "public"."occasiontype";
CREATE TYPE "public"."occasiontype" AS ENUM (
  'BIRTHDAY',
  'WEDDING',
  'ANNIVERSARY',
  'HOLIDAY',
  'CHRISTMAS',
  'VALENTINES',
  'GENERIC',
  'OTHER'
);

-- ----------------------------
-- Type structure for orderitemstatus
-- ----------------------------
DROP TYPE IF EXISTS "public"."orderitemstatus";
CREATE TYPE "public"."orderitemstatus" AS ENUM (
  'PENDING',
  'CONFIRMED',
  'PROCESSING',
  'READY_TO_SHIP',
  'PARTIALLY_SHIPPED',
  'SHIPPED',
  'DELIVERED',
  'CANCELLED',
  'RETURNED',
  'PARTIALLY_RETURNED'
);

-- ----------------------------
-- Type structure for orderstatus
-- ----------------------------
DROP TYPE IF EXISTS "public"."orderstatus";
CREATE TYPE "public"."orderstatus" AS ENUM (
  'PENDING',
  'PROCESSING',
  'AWAITING_PAYMENT',
  'PAID',
  'PARTIALLY_PAID',
  'SHIPPED',
  'PARTIALLY_SHIPPED',
  'DELIVERED',
  'COMPLETED',
  'CANCELLED',
  'REFUNDED',
  'PARTIALLY_REFUNDED',
  'ON_HOLD'
);

-- ----------------------------
-- Type structure for paymentmethodstatus
-- ----------------------------
DROP TYPE IF EXISTS "public"."paymentmethodstatus";
CREATE TYPE "public"."paymentmethodstatus" AS ENUM (
  'ACTIVE',
  'INACTIVE',
  'TESTING'
);

-- ----------------------------
-- Type structure for paymentresult
-- ----------------------------
DROP TYPE IF EXISTS "public"."paymentresult";
CREATE TYPE "public"."paymentresult" AS ENUM (
  'SUCCESS',
  'PENDING',
  'FAILED',
  'CANCELLED',
  'REFUNDED',
  'PARTIALLY_REFUNDED'
);

-- ----------------------------
-- Type structure for paymentstatus
-- ----------------------------
DROP TYPE IF EXISTS "public"."paymentstatus";
CREATE TYPE "public"."paymentstatus" AS ENUM (
  'PENDING',
  'PROCESSING',
  'PAID',
  'PARTIALLY_PAID',
  'FAILED',
  'REFUNDED',
  'PARTIALLY_REFUNDED',
  'CANCELLED'
);

-- ----------------------------
-- Type structure for paymentstatusenum
-- ----------------------------
DROP TYPE IF EXISTS "public"."paymentstatusenum";
CREATE TYPE "public"."paymentstatusenum" AS ENUM (
  'PENDING',
  'PROCESSING',
  'AUTHORIZED',
  'COMPLETED',
  'CANCELLED',
  'DECLINED',
  'REFUNDED',
  'PARTIALLY_REFUNDED',
  'FAILED',
  'EXPIRED',
  'WAITING'
);

-- ----------------------------
-- Type structure for paymenttype
-- ----------------------------
DROP TYPE IF EXISTS "public"."paymenttype";
CREATE TYPE "public"."paymenttype" AS ENUM (
  'CREDIT_CARD',
  'DEBIT_CARD',
  'PAYPAL',
  'BANK_TRANSFER',
  'COD',
  'WALLET',
  'CRYPTO',
  'GRABPAY',
  'SHOPEEPAY',
  'GOPAY',
  'DANA',
  'OVO',
  'LINEPAY',
  'MOMO',
  'OTHER'
);

-- ----------------------------
-- Type structure for productstatus
-- ----------------------------
DROP TYPE IF EXISTS "public"."productstatus";
CREATE TYPE "public"."productstatus" AS ENUM (
  'DRAFT',
  'ACTIVE',
  'INACTIVE',
  'DELETED'
);

-- ----------------------------
-- Type structure for promotiontype
-- ----------------------------
DROP TYPE IF EXISTS "public"."promotiontype";
CREATE TYPE "public"."promotiontype" AS ENUM (
  'CART_DISCOUNT',
  'PRODUCT_DISCOUNT',
  'BUY_X_GET_Y',
  'BUNDLE',
  'GIFT',
  'FREE_SHIPPING',
  'FLASH_SALE',
  'COUPON',
  'LOYALTY_POINTS',
  'THEMATIC',
  'SEASONAL'
);

-- ----------------------------
-- Type structure for registrationsource
-- ----------------------------
DROP TYPE IF EXISTS "public"."registrationsource";
CREATE TYPE "public"."registrationsource" AS ENUM (
  'WEBSITE',
  'MOBILE_APP',
  'FACEBOOK',
  'GOOGLE',
  'APPLE',
  'OFFLINE',
  'ADMIN'
);

-- ----------------------------
-- Type structure for registrystatus
-- ----------------------------
DROP TYPE IF EXISTS "public"."registrystatus";
CREATE TYPE "public"."registrystatus" AS ENUM (
  'ACTIVE',
  'INACTIVE',
  'COMPLETED',
  'EXPIRED',
  'ARCHIVED'
);

-- ----------------------------
-- Type structure for registrytype
-- ----------------------------
DROP TYPE IF EXISTS "public"."registrytype";
CREATE TYPE "public"."registrytype" AS ENUM (
  'WEDDING',
  'BABY_SHOWER',
  'BIRTHDAY',
  'ANNIVERSARY',
  'HOUSEWARMING',
  'GRADUATION',
  'OTHER'
);

-- ----------------------------
-- Type structure for returnaction
-- ----------------------------
DROP TYPE IF EXISTS "public"."returnaction";
CREATE TYPE "public"."returnaction" AS ENUM (
  'REFUND',
  'REPLACE',
  'REPAIR',
  'STORE_CREDIT',
  'EXCHANGE'
);

-- ----------------------------
-- Type structure for returnreason
-- ----------------------------
DROP TYPE IF EXISTS "public"."returnreason";
CREATE TYPE "public"."returnreason" AS ENUM (
  'DAMAGED',
  'DEFECTIVE',
  'NOT_AS_DESCRIBED',
  'WRONG_ITEM',
  'UNWANTED',
  'SIZE_ISSUE',
  'QUALITY_ISSUE',
  'LATE_DELIVERY',
  'OTHER'
);

-- ----------------------------
-- Type structure for returnstatus
-- ----------------------------
DROP TYPE IF EXISTS "public"."returnstatus";
CREATE TYPE "public"."returnstatus" AS ENUM (
  'PENDING',
  'APPROVED',
  'RECEIVED',
  'COMPLETED',
  'REJECTED',
  'CANCELLED',
  'PARTIALLY_REFUNDED',
  'REFUNDED'
);

-- ----------------------------
-- Type structure for shipmentstatus
-- ----------------------------
DROP TYPE IF EXISTS "public"."shipmentstatus";
CREATE TYPE "public"."shipmentstatus" AS ENUM (
  'PENDING',
  'PREPARING',
  'READY_TO_SHIP',
  'SHIPPED',
  'IN_TRANSIT',
  'OUT_FOR_DELIVERY',
  'DELIVERED',
  'FAILED',
  'RETURNED',
  'CANCELLED'
);

-- ----------------------------
-- Type structure for shippingmethodstatus
-- ----------------------------
DROP TYPE IF EXISTS "public"."shippingmethodstatus";
CREATE TYPE "public"."shippingmethodstatus" AS ENUM (
  'ACTIVE',
  'INACTIVE',
  'TESTING'
);

-- ----------------------------
-- Type structure for shippingstatus
-- ----------------------------
DROP TYPE IF EXISTS "public"."shippingstatus";
CREATE TYPE "public"."shippingstatus" AS ENUM (
  'PENDING',
  'PROCESSING',
  'PARTIALLY_SHIPPED',
  'SHIPPED',
  'DELIVERED',
  'FAILED',
  'RETURNED'
);

-- ----------------------------
-- Type structure for trackingeventtype
-- ----------------------------
DROP TYPE IF EXISTS "public"."trackingeventtype";
CREATE TYPE "public"."trackingeventtype" AS ENUM (
  'PICKED_UP',
  'IN_TRANSIT',
  'ARRIVED_AT_FACILITY',
  'OUT_FOR_DELIVERY',
  'DELIVERED',
  'DELIVERY_ATTEMPTED',
  'EXCEPTION',
  'RETURNED'
);

-- ----------------------------
-- Type structure for trackingstatus
-- ----------------------------
DROP TYPE IF EXISTS "public"."trackingstatus";
CREATE TYPE "public"."trackingstatus" AS ENUM (
  'CREATED',
  'PICKED_UP',
  'IN_TRANSIT',
  'ARRIVED_AT_FACILITY',
  'OUT_FOR_DELIVERY',
  'DELIVERED',
  'DELIVERY_FAILED',
  'RETURNED'
);

-- ----------------------------
-- Type structure for transactionstatus
-- ----------------------------
DROP TYPE IF EXISTS "public"."transactionstatus";
CREATE TYPE "public"."transactionstatus" AS ENUM (
  'PENDING',
  'SUCCESS',
  'FAILED',
  'CANCELLED',
  'REFUNDED',
  'PARTIALLY_REFUNDED',
  'AUTHORIZED',
  'CAPTURED',
  'VOIDED',
  'EXPIRED'
);

-- ----------------------------
-- Type structure for transactiontype
-- ----------------------------
DROP TYPE IF EXISTS "public"."transactiontype";
CREATE TYPE "public"."transactiontype" AS ENUM (
  'PAYMENT',
  'REFUND',
  'AUTHORIZATION',
  'CAPTURE',
  'VOID'
);

-- ----------------------------
-- Table structure for blacklists
-- ----------------------------
DROP TABLE IF EXISTS "public"."blacklists";
CREATE TABLE "public"."blacklists" (
  "id" uuid NOT NULL,
  "blacklist_type" varchar(20) COLLATE "pg_catalog"."default" NOT NULL,
  "value" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "reason" text COLLATE "pg_catalog"."default",
  "notes" text COLLATE "pg_catalog"."default",
  "is_active" bool,
  "created_by" uuid,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."blacklists"."blacklist_type" IS '黑名单类型，如email, phone, address, ip';
COMMENT ON COLUMN "public"."blacklists"."value" IS '黑名单值';
COMMENT ON COLUMN "public"."blacklists"."reason" IS '拉黑原因';
COMMENT ON COLUMN "public"."blacklists"."notes" IS '备注';
COMMENT ON COLUMN "public"."blacklists"."is_active" IS '是否生效';

-- ----------------------------
-- Records of blacklists
-- ----------------------------

-- ----------------------------
-- Table structure for bundle_intent
-- ----------------------------
DROP TABLE IF EXISTS "public"."bundle_intent";
CREATE TABLE "public"."bundle_intent" (
  "bundle_id" uuid NOT NULL,
  "intent_id" uuid NOT NULL,
  "created_at" timestamp(6) NOT NULL
)
;

-- ----------------------------
-- Records of bundle_intent
-- ----------------------------

-- ----------------------------
-- Table structure for bundle_items
-- ----------------------------
DROP TABLE IF EXISTS "public"."bundle_items";
CREATE TABLE "public"."bundle_items" (
  "id" uuid NOT NULL,
  "bundle_id" uuid NOT NULL,
  "product_id" uuid NOT NULL,
  "sku_id" uuid,
  "quantity" int4 NOT NULL,
  "sort_order" int4,
  "discount_type" varchar(20) COLLATE "pg_catalog"."default",
  "discount_value" float8,
  "is_mandatory" bool,
  "description" text COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."bundle_items"."quantity" IS '数量';
COMMENT ON COLUMN "public"."bundle_items"."sort_order" IS '排序顺序';
COMMENT ON COLUMN "public"."bundle_items"."discount_type" IS '单品折扣类型：percentage, fixed_amount';
COMMENT ON COLUMN "public"."bundle_items"."discount_value" IS '单品折扣值';
COMMENT ON COLUMN "public"."bundle_items"."is_mandatory" IS '是否必选项';
COMMENT ON COLUMN "public"."bundle_items"."description" IS '说明';

-- ----------------------------
-- Records of bundle_items
-- ----------------------------

-- ----------------------------
-- Table structure for bundle_theme
-- ----------------------------
DROP TABLE IF EXISTS "public"."bundle_theme";
CREATE TABLE "public"."bundle_theme" (
  "bundle_id" uuid NOT NULL,
  "theme_id" uuid NOT NULL,
  "created_at" timestamp(6) NOT NULL
)
;

-- ----------------------------
-- Records of bundle_theme
-- ----------------------------

-- ----------------------------
-- Table structure for carriers
-- ----------------------------
DROP TABLE IF EXISTS "public"."carriers";
CREATE TABLE "public"."carriers" (
  "id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "code" varchar(20) COLLATE "pg_catalog"."default" NOT NULL,
  "contact_phone" varchar(30) COLLATE "pg_catalog"."default",
  "contact_email" varchar(100) COLLATE "pg_catalog"."default",
  "website" varchar(255) COLLATE "pg_catalog"."default",
  "tracking_url_template" varchar(500) COLLATE "pg_catalog"."default",
  "supported_countries" jsonb,
  "service_types" jsonb,
  "api_endpoint" varchar(255) COLLATE "pg_catalog"."default",
  "api_key" varchar(255) COLLATE "pg_catalog"."default",
  "api_config" jsonb,
  "is_active" bool DEFAULT true,
  "priority" int4 DEFAULT 0,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of carriers
-- ----------------------------

-- ----------------------------
-- Table structure for cash_on_delivery_settings
-- ----------------------------
DROP TABLE IF EXISTS "public"."cash_on_delivery_settings";
CREATE TABLE "public"."cash_on_delivery_settings" (
  "id" uuid NOT NULL,
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default",
  "is_active" bool,
  "allowed_countries" varchar[] COLLATE "pg_catalog"."default",
  "allowed_regions" json,
  "excluded_postcodes" varchar[] COLLATE "pg_catalog"."default",
  "min_order_amount" float8,
  "max_order_amount" float8,
  "fee_type" varchar(20) COLLATE "pg_catalog"."default",
  "fee_amount" float8,
  "fee_percentage" float8,
  "min_fee" float8,
  "max_fee" float8,
  "excluded_product_categories" uuid[],
  "excluded_products" uuid[],
  "max_product_weight" float8,
  "max_product_dimensions" json,
  "allowed_customer_groups" uuid[],
  "min_customer_orders" int4,
  "requires_verification_call" bool,
  "requires_id_verification" bool,
  "blacklisted_customers" uuid[],
  "allowed_shipping_methods" uuid[],
  "delivery_timeframe" varchar(100) COLLATE "pg_catalog"."default",
  "collection_timeframe" varchar(100) COLLATE "pg_catalog"."default",
  "return_policy" text COLLATE "pg_catalog"."default",
  "notification_emails" varchar[] COLLATE "pg_catalog"."default",
  "email_template" text COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."cash_on_delivery_settings"."name" IS '设置名称';
COMMENT ON COLUMN "public"."cash_on_delivery_settings"."description" IS '设置描述';
COMMENT ON COLUMN "public"."cash_on_delivery_settings"."is_active" IS '是否激活';
COMMENT ON COLUMN "public"."cash_on_delivery_settings"."allowed_countries" IS '允许的国家代码列表';
COMMENT ON COLUMN "public"."cash_on_delivery_settings"."allowed_regions" IS '允许的区域详情，如{country: [regions]}格式';
COMMENT ON COLUMN "public"."cash_on_delivery_settings"."excluded_postcodes" IS '排除的邮编列表';
COMMENT ON COLUMN "public"."cash_on_delivery_settings"."min_order_amount" IS '最小订单金额';
COMMENT ON COLUMN "public"."cash_on_delivery_settings"."max_order_amount" IS '最大订单金额';
COMMENT ON COLUMN "public"."cash_on_delivery_settings"."fee_type" IS '费用类型：fixed, percentage, mixed';
COMMENT ON COLUMN "public"."cash_on_delivery_settings"."fee_amount" IS '固定费用金额';
COMMENT ON COLUMN "public"."cash_on_delivery_settings"."fee_percentage" IS '百分比费用';
COMMENT ON COLUMN "public"."cash_on_delivery_settings"."min_fee" IS '最小费用';
COMMENT ON COLUMN "public"."cash_on_delivery_settings"."max_fee" IS '最大费用';
COMMENT ON COLUMN "public"."cash_on_delivery_settings"."excluded_product_categories" IS '排除的产品分类ID列表';
COMMENT ON COLUMN "public"."cash_on_delivery_settings"."excluded_products" IS '排除的产品ID列表';
COMMENT ON COLUMN "public"."cash_on_delivery_settings"."max_product_weight" IS '最大产品重量(克)';
COMMENT ON COLUMN "public"."cash_on_delivery_settings"."max_product_dimensions" IS '最大产品尺寸，如{length, width, height}格式';
COMMENT ON COLUMN "public"."cash_on_delivery_settings"."allowed_customer_groups" IS '允许的客户组ID列表';
COMMENT ON COLUMN "public"."cash_on_delivery_settings"."min_customer_orders" IS '客户最小历史订单数';
COMMENT ON COLUMN "public"."cash_on_delivery_settings"."requires_verification_call" IS '是否需要电话验证';
COMMENT ON COLUMN "public"."cash_on_delivery_settings"."requires_id_verification" IS '是否需要身份验证';
COMMENT ON COLUMN "public"."cash_on_delivery_settings"."blacklisted_customers" IS '黑名单客户ID列表';
COMMENT ON COLUMN "public"."cash_on_delivery_settings"."allowed_shipping_methods" IS '允许的配送方式ID列表';
COMMENT ON COLUMN "public"."cash_on_delivery_settings"."delivery_timeframe" IS '配送时间范围';
COMMENT ON COLUMN "public"."cash_on_delivery_settings"."collection_timeframe" IS '收款时间范围';
COMMENT ON COLUMN "public"."cash_on_delivery_settings"."return_policy" IS '退货政策';
COMMENT ON COLUMN "public"."cash_on_delivery_settings"."notification_emails" IS '通知邮箱列表';
COMMENT ON COLUMN "public"."cash_on_delivery_settings"."email_template" IS '邮件模板';

-- ----------------------------
-- Records of cash_on_delivery_settings
-- ----------------------------

-- ----------------------------
-- Table structure for coupon_batches
-- ----------------------------
DROP TABLE IF EXISTS "public"."coupon_batches";
CREATE TABLE "public"."coupon_batches" (
  "id" uuid NOT NULL,
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default",
  "code_prefix" varchar(10) COLLATE "pg_catalog"."default",
  "code_format" "public"."couponformat",
  "code_length" int4,
  "quantity" int4 NOT NULL,
  "generated_count" int4,
  "used_count" int4,
  "max_uses_per_coupon" int4,
  "valid_from" timestamp(6) NOT NULL,
  "valid_to" timestamp(6),
  "is_exported" bool,
  "export_date" timestamp(6),
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."coupon_batches"."name" IS '批次名称';
COMMENT ON COLUMN "public"."coupon_batches"."description" IS '批次描述';
COMMENT ON COLUMN "public"."coupon_batches"."code_prefix" IS '前缀';
COMMENT ON COLUMN "public"."coupon_batches"."code_format" IS '优惠码格式';
COMMENT ON COLUMN "public"."coupon_batches"."code_length" IS '优惠码长度';
COMMENT ON COLUMN "public"."coupon_batches"."quantity" IS '生成数量';
COMMENT ON COLUMN "public"."coupon_batches"."generated_count" IS '已生成数量';
COMMENT ON COLUMN "public"."coupon_batches"."used_count" IS '已使用数量';
COMMENT ON COLUMN "public"."coupon_batches"."max_uses_per_coupon" IS '每个优惠券最大使用次数';
COMMENT ON COLUMN "public"."coupon_batches"."valid_from" IS '有效期开始';
COMMENT ON COLUMN "public"."coupon_batches"."valid_to" IS '有效期结束';
COMMENT ON COLUMN "public"."coupon_batches"."is_exported" IS '是否已导出';
COMMENT ON COLUMN "public"."coupon_batches"."export_date" IS '导出日期';

-- ----------------------------
-- Records of coupon_batches
-- ----------------------------

-- ----------------------------
-- Table structure for coupons
-- ----------------------------
DROP TABLE IF EXISTS "public"."coupons";
CREATE TABLE "public"."coupons" (
  "id" uuid NOT NULL,
  "promotion_id" uuid NOT NULL,
  "code" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "status" "public"."couponstatus" NOT NULL,
  "format" "public"."couponformat",
  "prefix" varchar(10) COLLATE "pg_catalog"."default",
  "suffix" varchar(10) COLLATE "pg_catalog"."default",
  "length" int4,
  "max_uses" int4,
  "max_uses_per_customer" int4,
  "current_uses" int4,
  "is_single_use" bool,
  "requires_authentication" bool,
  "valid_from" timestamp(6) NOT NULL,
  "valid_to" timestamp(6),
  "is_batch" bool,
  "batch_id" uuid,
  "is_referral" bool,
  "referrer_reward" float8,
  "is_public" bool,
  "is_featured" bool,
  "auto_apply" bool,
  "free_product_id" uuid,
  "free_product_quantity" int4,
  "view_count" int4,
  "conversion_rate" float8,
  "meta_data" json,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."coupons"."code" IS '优惠码';
COMMENT ON COLUMN "public"."coupons"."status" IS '状态';
COMMENT ON COLUMN "public"."coupons"."format" IS '优惠码格式';
COMMENT ON COLUMN "public"."coupons"."prefix" IS '前缀';
COMMENT ON COLUMN "public"."coupons"."suffix" IS '后缀';
COMMENT ON COLUMN "public"."coupons"."length" IS '长度';
COMMENT ON COLUMN "public"."coupons"."max_uses" IS '最大使用次数，空表示不限制';
COMMENT ON COLUMN "public"."coupons"."max_uses_per_customer" IS '每个客户最大使用次数';
COMMENT ON COLUMN "public"."coupons"."current_uses" IS '当前使用次数';
COMMENT ON COLUMN "public"."coupons"."is_single_use" IS '是否一次性使用';
COMMENT ON COLUMN "public"."coupons"."requires_authentication" IS '是否需要用户登录';
COMMENT ON COLUMN "public"."coupons"."valid_from" IS '有效期开始';
COMMENT ON COLUMN "public"."coupons"."valid_to" IS '有效期结束，空表示永久有效';
COMMENT ON COLUMN "public"."coupons"."is_batch" IS '是否批量优惠券';
COMMENT ON COLUMN "public"."coupons"."is_referral" IS '是否推荐优惠券';
COMMENT ON COLUMN "public"."coupons"."referrer_reward" IS '推荐人奖励';
COMMENT ON COLUMN "public"."coupons"."is_public" IS '是否公开可用（无需特定分发）';
COMMENT ON COLUMN "public"."coupons"."is_featured" IS '是否推荐显示';
COMMENT ON COLUMN "public"."coupons"."auto_apply" IS '是否自动应用';
COMMENT ON COLUMN "public"."coupons"."free_product_quantity" IS '赠品数量';
COMMENT ON COLUMN "public"."coupons"."view_count" IS '查看次数';
COMMENT ON COLUMN "public"."coupons"."conversion_rate" IS '转化率';
COMMENT ON COLUMN "public"."coupons"."meta_data" IS '元数据';

-- ----------------------------
-- Records of coupons
-- ----------------------------

-- ----------------------------
-- Table structure for currencies
-- ----------------------------
DROP TABLE IF EXISTS "public"."currencies";
CREATE TABLE "public"."currencies" (
  "id" uuid NOT NULL,
  "code" varchar(3) COLLATE "pg_catalog"."default" NOT NULL,
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "symbol" varchar(10) COLLATE "pg_catalog"."default",
  "decimal_places" int4,
  "decimal_separator" varchar(1) COLLATE "pg_catalog"."default",
  "thousand_separator" varchar(1) COLLATE "pg_catalog"."default",
  "symbol_position" varchar(10) COLLATE "pg_catalog"."default",
  "format_pattern" varchar(50) COLLATE "pg_catalog"."default",
  "is_active" bool,
  "is_base_currency" bool,
  "is_default" bool,
  "countries" json,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."currencies"."code" IS '货币代码（ISO 4217）';
COMMENT ON COLUMN "public"."currencies"."name" IS '货币名称';
COMMENT ON COLUMN "public"."currencies"."symbol" IS '货币符号';
COMMENT ON COLUMN "public"."currencies"."decimal_places" IS '小数位数';
COMMENT ON COLUMN "public"."currencies"."decimal_separator" IS '小数分隔符';
COMMENT ON COLUMN "public"."currencies"."thousand_separator" IS '千位分隔符';
COMMENT ON COLUMN "public"."currencies"."symbol_position" IS '符号位置：before, after';
COMMENT ON COLUMN "public"."currencies"."format_pattern" IS '格式模式，如 %s%v';
COMMENT ON COLUMN "public"."currencies"."is_active" IS '是否激活';
COMMENT ON COLUMN "public"."currencies"."is_base_currency" IS '是否基础货币';
COMMENT ON COLUMN "public"."currencies"."is_default" IS '是否默认货币';
COMMENT ON COLUMN "public"."currencies"."countries" IS '使用此货币的国家';

-- ----------------------------
-- Records of currencies
-- ----------------------------

-- ----------------------------
-- Table structure for currency_rates
-- ----------------------------
DROP TABLE IF EXISTS "public"."currency_rates";
CREATE TABLE "public"."currency_rates" (
  "id" uuid NOT NULL,
  "from_currency" varchar(3) COLLATE "pg_catalog"."default" NOT NULL,
  "to_currency" varchar(3) COLLATE "pg_catalog"."default" NOT NULL,
  "rate" float8 NOT NULL,
  "inverse_rate" float8 NOT NULL,
  "source" varchar(100) COLLATE "pg_catalog"."default",
  "source_timestamp" timestamp(6),
  "is_active" bool,
  "effective_date" timestamp(6) NOT NULL,
  "expiry_date" timestamp(6),
  "is_manual" bool,
  "is_default" bool,
  "manual_adjustment" float8,
  "bid_rate" float8,
  "ask_rate" float8,
  "mid_rate" float8,
  "meta_data" json,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."currency_rates"."from_currency" IS '源货币代码';
COMMENT ON COLUMN "public"."currency_rates"."to_currency" IS '目标货币代码';
COMMENT ON COLUMN "public"."currency_rates"."rate" IS '汇率';
COMMENT ON COLUMN "public"."currency_rates"."inverse_rate" IS '反向汇率';
COMMENT ON COLUMN "public"."currency_rates"."source" IS '数据来源';
COMMENT ON COLUMN "public"."currency_rates"."source_timestamp" IS '源数据时间戳';
COMMENT ON COLUMN "public"."currency_rates"."is_active" IS '是否激活';
COMMENT ON COLUMN "public"."currency_rates"."effective_date" IS '生效日期';
COMMENT ON COLUMN "public"."currency_rates"."expiry_date" IS '过期日期';
COMMENT ON COLUMN "public"."currency_rates"."is_manual" IS '是否手动设置';
COMMENT ON COLUMN "public"."currency_rates"."is_default" IS '是否默认汇率';
COMMENT ON COLUMN "public"."currency_rates"."manual_adjustment" IS '手动调整百分比';
COMMENT ON COLUMN "public"."currency_rates"."bid_rate" IS '买入汇率';
COMMENT ON COLUMN "public"."currency_rates"."ask_rate" IS '卖出汇率';
COMMENT ON COLUMN "public"."currency_rates"."mid_rate" IS '中间汇率';
COMMENT ON COLUMN "public"."currency_rates"."meta_data" IS '元数据';

-- ----------------------------
-- Records of currency_rates
-- ----------------------------

-- ----------------------------
-- Table structure for customer_addresses
-- ----------------------------
DROP TABLE IF EXISTS "public"."customer_addresses";
CREATE TABLE "public"."customer_addresses" (
  "id" uuid NOT NULL,
  "customer_id" uuid NOT NULL,
  "address_type" "public"."addresstype" NOT NULL,
  "is_default" bool,
  "first_name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "last_name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "company_name" varchar(100) COLLATE "pg_catalog"."default",
  "phone_number" varchar(20) COLLATE "pg_catalog"."default" NOT NULL,
  "email" varchar(255) COLLATE "pg_catalog"."default",
  "address_line1" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "address_line2" varchar(255) COLLATE "pg_catalog"."default",
  "city" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "state_province" varchar(100) COLLATE "pg_catalog"."default",
  "postal_code" varchar(20) COLLATE "pg_catalog"."default" NOT NULL,
  "country_code" varchar(2) COLLATE "pg_catalog"."default" NOT NULL,
  "delivery_notes" text COLLATE "pg_catalog"."default",
  "latitude" float8,
  "longitude" float8,
  "is_verified" bool,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."customer_addresses"."is_default" IS '是否为默认地址';
COMMENT ON COLUMN "public"."customer_addresses"."country_code" IS 'ISO国家代码，如US';
COMMENT ON COLUMN "public"."customer_addresses"."delivery_notes" IS '送货注意事项';

-- ----------------------------
-- Records of customer_addresses
-- ----------------------------
INSERT INTO "public"."customer_addresses" VALUES ('ca1c8644-5922-4868-b2c4-7ae38cb3c9c5', '6c78b575-cd35-414a-a400-d75b46677f2a', 'SHIPPING', 't', 'Jinyuan', 'li', '', '18180055588', NULL, 'jiuxiangshifang 5-302', '', 'meishan', 'sichuan', '610010', 'CN', NULL, NULL, NULL, 'f', '2025-06-06 03:38:32.787663', '2025-06-06 03:38:32.787663');

-- ----------------------------
-- Table structure for customer_behaviors
-- ----------------------------
DROP TABLE IF EXISTS "public"."customer_behaviors";
CREATE TABLE "public"."customer_behaviors" (
  "id" uuid NOT NULL,
  "customer_id" uuid NOT NULL,
  "behavior_type" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "entity_type" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "entity_id" uuid NOT NULL,
  "meta_data" json,
  "user_agent" varchar(255) COLLATE "pg_catalog"."default",
  "ip_address" varchar(50) COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."customer_behaviors"."behavior_type" IS '行为类型，如view_product, add_to_cart等';
COMMENT ON COLUMN "public"."customer_behaviors"."entity_type" IS '实体类型，如product, category等';
COMMENT ON COLUMN "public"."customer_behaviors"."entity_id" IS '实体ID';
COMMENT ON COLUMN "public"."customer_behaviors"."meta_data" IS '元数据，如停留时间、点击位置等';
COMMENT ON COLUMN "public"."customer_behaviors"."user_agent" IS '用户代理';

-- ----------------------------
-- Records of customer_behaviors
-- ----------------------------

-- ----------------------------
-- Table structure for customer_coupons
-- ----------------------------
DROP TABLE IF EXISTS "public"."customer_coupons";
CREATE TABLE "public"."customer_coupons" (
  "id" uuid NOT NULL,
  "customer_id" uuid NOT NULL,
  "coupon_id" uuid NOT NULL,
  "status" "public"."customercouponstatus" NOT NULL,
  "issue_method" "public"."issuemethod" NOT NULL,
  "issued_by" uuid,
  "issued_at" timestamp(6) NOT NULL,
  "used_at" timestamp(6),
  "order_id" uuid,
  "discount_amount" float8,
  "valid_from" timestamp(6),
  "valid_to" timestamp(6),
  "notification_sent" bool,
  "notification_method" varchar(50) COLLATE "pg_catalog"."default",
  "referrer_id" uuid,
  "custom_message" text COLLATE "pg_catalog"."default",
  "notes" text COLLATE "pg_catalog"."default",
  "meta_data" json,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."customer_coupons"."status" IS '状态';
COMMENT ON COLUMN "public"."customer_coupons"."issue_method" IS '发放方式';
COMMENT ON COLUMN "public"."customer_coupons"."issued_by" IS '发放人';
COMMENT ON COLUMN "public"."customer_coupons"."issued_at" IS '发放时间';
COMMENT ON COLUMN "public"."customer_coupons"."used_at" IS '使用时间';
COMMENT ON COLUMN "public"."customer_coupons"."order_id" IS '使用订单';
COMMENT ON COLUMN "public"."customer_coupons"."discount_amount" IS '折扣金额';
COMMENT ON COLUMN "public"."customer_coupons"."valid_from" IS '有效期开始';
COMMENT ON COLUMN "public"."customer_coupons"."valid_to" IS '有效期结束';
COMMENT ON COLUMN "public"."customer_coupons"."notification_sent" IS '是否已发送通知';
COMMENT ON COLUMN "public"."customer_coupons"."notification_method" IS '通知方式';
COMMENT ON COLUMN "public"."customer_coupons"."referrer_id" IS '推荐人';
COMMENT ON COLUMN "public"."customer_coupons"."custom_message" IS '自定义消息';
COMMENT ON COLUMN "public"."customer_coupons"."notes" IS '备注';
COMMENT ON COLUMN "public"."customer_coupons"."meta_data" IS '元数据';

-- ----------------------------
-- Records of customer_coupons
-- ----------------------------

-- ----------------------------
-- Table structure for customer_cultural_preference
-- ----------------------------
DROP TABLE IF EXISTS "public"."customer_cultural_preference";
CREATE TABLE "public"."customer_cultural_preference" (
  "customer_id" uuid NOT NULL,
  "symbol_id" uuid NOT NULL,
  "preference_level" int4,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."customer_cultural_preference"."preference_level" IS '偏好程度，1-5';

-- ----------------------------
-- Records of customer_cultural_preference
-- ----------------------------

-- ----------------------------
-- Table structure for customer_cultural_preference_details
-- ----------------------------
DROP TABLE IF EXISTS "public"."customer_cultural_preference_details";
CREATE TABLE "public"."customer_cultural_preference_details" (
  "id" uuid NOT NULL,
  "customer_id" uuid NOT NULL,
  "symbol_id" uuid NOT NULL,
  "preference_level" int4,
  "confidence_score" float8,
  "engagement_count" int4,
  "last_engagement_at" timestamp(6),
  "notes" text COLLATE "pg_catalog"."default",
  "source" varchar(50) COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."customer_cultural_preference_details"."preference_level" IS '偏好程度，1-5级';
COMMENT ON COLUMN "public"."customer_cultural_preference_details"."confidence_score" IS '置信度分数，0-1之间';
COMMENT ON COLUMN "public"."customer_cultural_preference_details"."engagement_count" IS '互动次数';
COMMENT ON COLUMN "public"."customer_cultural_preference_details"."last_engagement_at" IS '最后互动时间';
COMMENT ON COLUMN "public"."customer_cultural_preference_details"."notes" IS '备注';
COMMENT ON COLUMN "public"."customer_cultural_preference_details"."source" IS '偏好来源，如browse, survey, purchase等';

-- ----------------------------
-- Records of customer_cultural_preference_details
-- ----------------------------

-- ----------------------------
-- Table structure for customer_group
-- ----------------------------
DROP TABLE IF EXISTS "public"."customer_group";
CREATE TABLE "public"."customer_group" (
  "customer_id" uuid NOT NULL,
  "group_id" uuid NOT NULL,
  "created_at" timestamp(6) NOT NULL
)
;

-- ----------------------------
-- Records of customer_group
-- ----------------------------

-- ----------------------------
-- Table structure for customer_groups
-- ----------------------------
DROP TABLE IF EXISTS "public"."customer_groups";
CREATE TABLE "public"."customer_groups" (
  "id" uuid NOT NULL,
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default",
  "is_system" bool,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."customer_groups"."is_system" IS '是否系统预定义分组';

-- ----------------------------
-- Records of customer_groups
-- ----------------------------

-- ----------------------------
-- Table structure for customer_intent
-- ----------------------------
DROP TABLE IF EXISTS "public"."customer_intent";
CREATE TABLE "public"."customer_intent" (
  "customer_id" uuid NOT NULL,
  "intent_id" uuid NOT NULL,
  "preference_level" int4,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."customer_intent"."preference_level" IS '偏好程度，1-5';

-- ----------------------------
-- Records of customer_intent
-- ----------------------------

-- ----------------------------
-- Table structure for customer_intent_details
-- ----------------------------
DROP TABLE IF EXISTS "public"."customer_intent_details";
CREATE TABLE "public"."customer_intent_details" (
  "id" uuid NOT NULL,
  "customer_id" uuid NOT NULL,
  "intent_id" uuid NOT NULL,
  "preference_level" int4,
  "confidence_score" float8,
  "engagement_count" int4,
  "last_engagement_at" timestamp(6),
  "notes" text COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."customer_intent_details"."preference_level" IS '偏好程度，1-5级';
COMMENT ON COLUMN "public"."customer_intent_details"."confidence_score" IS '置信度分数，0-1之间';
COMMENT ON COLUMN "public"."customer_intent_details"."engagement_count" IS '互动次数';
COMMENT ON COLUMN "public"."customer_intent_details"."last_engagement_at" IS '最后互动时间';
COMMENT ON COLUMN "public"."customer_intent_details"."notes" IS '备注';

-- ----------------------------
-- Records of customer_intent_details
-- ----------------------------

-- ----------------------------
-- Table structure for customer_points
-- ----------------------------
DROP TABLE IF EXISTS "public"."customer_points";
CREATE TABLE "public"."customer_points" (
  "id" uuid NOT NULL,
  "customer_id" uuid NOT NULL,
  "amount" int4 NOT NULL,
  "description" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "transaction_type" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "reference_type" varchar(50) COLLATE "pg_catalog"."default",
  "reference_id" uuid,
  "expiry_date" timestamp(6),
  "is_expired" bool,
  "created_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."customer_points"."amount" IS '积分数量，正数为获取，负数为使用';
COMMENT ON COLUMN "public"."customer_points"."description" IS '积分描述，如购物获得、积分兑换等';
COMMENT ON COLUMN "public"."customer_points"."transaction_type" IS '交易类型，如earn, redeem, expire';
COMMENT ON COLUMN "public"."customer_points"."reference_type" IS '关联类型，如order, promotion等';
COMMENT ON COLUMN "public"."customer_points"."reference_id" IS '关联ID';
COMMENT ON COLUMN "public"."customer_points"."expiry_date" IS '过期时间';
COMMENT ON COLUMN "public"."customer_points"."is_expired" IS '是否已过期';

-- ----------------------------
-- Records of customer_points
-- ----------------------------

-- ----------------------------
-- Table structure for customer_scene_preference
-- ----------------------------
DROP TABLE IF EXISTS "public"."customer_scene_preference";
CREATE TABLE "public"."customer_scene_preference" (
  "customer_id" uuid NOT NULL,
  "scene_id" uuid NOT NULL,
  "preference_level" int4,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."customer_scene_preference"."preference_level" IS '偏好程度，1-5';

-- ----------------------------
-- Records of customer_scene_preference
-- ----------------------------

-- ----------------------------
-- Table structure for customer_scene_preference_details
-- ----------------------------
DROP TABLE IF EXISTS "public"."customer_scene_preference_details";
CREATE TABLE "public"."customer_scene_preference_details" (
  "id" uuid NOT NULL,
  "customer_id" uuid NOT NULL,
  "scene_id" uuid NOT NULL,
  "preference_level" int4,
  "confidence_score" float8,
  "engagement_count" int4,
  "last_engagement_at" timestamp(6),
  "notes" text COLLATE "pg_catalog"."default",
  "source" varchar(50) COLLATE "pg_catalog"."default",
  "frequency_of_use" varchar(50) COLLATE "pg_catalog"."default",
  "expertise_level" varchar(50) COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."customer_scene_preference_details"."preference_level" IS '偏好程度，1-5级';
COMMENT ON COLUMN "public"."customer_scene_preference_details"."confidence_score" IS '置信度分数，0-1之间';
COMMENT ON COLUMN "public"."customer_scene_preference_details"."engagement_count" IS '互动次数';
COMMENT ON COLUMN "public"."customer_scene_preference_details"."last_engagement_at" IS '最后互动时间';
COMMENT ON COLUMN "public"."customer_scene_preference_details"."notes" IS '备注';
COMMENT ON COLUMN "public"."customer_scene_preference_details"."source" IS '偏好来源，如browse, survey, purchase等';
COMMENT ON COLUMN "public"."customer_scene_preference_details"."frequency_of_use" IS '使用频率，如daily, weekly, monthly';
COMMENT ON COLUMN "public"."customer_scene_preference_details"."expertise_level" IS '专业程度，如beginner, intermediate, expert';

-- ----------------------------
-- Records of customer_scene_preference_details
-- ----------------------------

-- ----------------------------
-- Table structure for customer_segments
-- ----------------------------
DROP TABLE IF EXISTS "public"."customer_segments";
CREATE TABLE "public"."customer_segments" (
  "id" uuid NOT NULL,
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default",
  "segment_type" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "is_dynamic" bool,
  "conditions" json,
  "attributes" json,
  "tags" varchar[] COLLATE "pg_catalog"."default",
  "is_active" bool,
  "customer_count" int4,
  "last_updated_at" timestamp(6),
  "last_campaign_at" timestamp(6),
  "created_by" uuid,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."customer_segments"."name" IS '细分名称';
COMMENT ON COLUMN "public"."customer_segments"."description" IS '细分描述';
COMMENT ON COLUMN "public"."customer_segments"."segment_type" IS '细分类型，如dynamic, static, hybrid';
COMMENT ON COLUMN "public"."customer_segments"."is_dynamic" IS '是否动态细分，根据条件自动更新';
COMMENT ON COLUMN "public"."customer_segments"."conditions" IS '细分条件，用于动态细分';
COMMENT ON COLUMN "public"."customer_segments"."attributes" IS '细分属性';
COMMENT ON COLUMN "public"."customer_segments"."tags" IS '标签';
COMMENT ON COLUMN "public"."customer_segments"."is_active" IS '是否激活';
COMMENT ON COLUMN "public"."customer_segments"."customer_count" IS '客户数量';
COMMENT ON COLUMN "public"."customer_segments"."last_updated_at" IS '最后更新时间';
COMMENT ON COLUMN "public"."customer_segments"."last_campaign_at" IS '最后营销活动时间';

-- ----------------------------
-- Records of customer_segments
-- ----------------------------

-- ----------------------------
-- Table structure for customers
-- ----------------------------
DROP TABLE IF EXISTS "public"."customers";
CREATE TABLE "public"."customers" (
  "id" uuid NOT NULL,
  "email" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "password_hash" varchar(255) COLLATE "pg_catalog"."default",
  "first_name" varchar(100) COLLATE "pg_catalog"."default",
  "last_name" varchar(100) COLLATE "pg_catalog"."default",
  "phone_number" varchar(20) COLLATE "pg_catalog"."default",
  "birth_date" date,
  "gender" varchar(20) COLLATE "pg_catalog"."default",
  "status" "public"."customerstatus" NOT NULL,
  "membership_level" "public"."membershiplevel" NOT NULL,
  "current_points" int4 NOT NULL,
  "total_points_earned" int4 NOT NULL,
  "registration_source" "public"."registrationsource" NOT NULL,
  "registration_ip" varchar(50) COLLATE "pg_catalog"."default",
  "last_login_at" timestamp(6),
  "last_login_ip" varchar(50) COLLATE "pg_catalog"."default",
  "notes" text COLLATE "pg_catalog"."default",
  "preferences" json,
  "language_preference" varchar(10) COLLATE "pg_catalog"."default",
  "currency_preference" varchar(3) COLLATE "pg_catalog"."default",
  "is_verified" bool,
  "referral_code" varchar(20) COLLATE "pg_catalog"."default",
  "referred_by" uuid,
  "verification_token" varchar(100) COLLATE "pg_catalog"."default",
  "verification_token_expires_at" timestamp(6),
  "reset_password_token" varchar(100) COLLATE "pg_catalog"."default",
  "reset_password_token_expires_at" timestamp(6),
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."customers"."current_points" IS '当前可用积分';
COMMENT ON COLUMN "public"."customers"."total_points_earned" IS '累计获得的积分';
COMMENT ON COLUMN "public"."customers"."notes" IS '管理员备注';
COMMENT ON COLUMN "public"."customers"."preferences" IS '用户偏好设置，如通知设置、隐私设置等';
COMMENT ON COLUMN "public"."customers"."language_preference" IS '语言偏好，如en-US';
COMMENT ON COLUMN "public"."customers"."currency_preference" IS '货币偏好，如USD';
COMMENT ON COLUMN "public"."customers"."is_verified" IS '电子邮件或手机是否已验证';
COMMENT ON COLUMN "public"."customers"."referral_code" IS '推荐码';
COMMENT ON COLUMN "public"."customers"."referred_by" IS '推荐人ID';

-- ----------------------------
-- Records of customers
-- ----------------------------
INSERT INTO "public"."customers" VALUES ('d1619fc9-550c-4208-bf4b-5c4553ed99dd', 'test@example.com', NULL, 'Test', 'User', '18180055588', NULL, NULL, 'ACTIVE', 'REGULAR', 0, 0, 'WEBSITE', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'f', 'L175OZZI', NULL, NULL, NULL, NULL, NULL, '2025-06-06 13:13:21.306722', '2025-06-06 13:13:21.306722');
INSERT INTO "public"."customers" VALUES ('c39e8faa-1fb0-48fb-91a5-84a3c5920f35', 'lixiaoming@example.com', NULL, '李小明', '', '13912345678', NULL, NULL, 'ACTIVE', 'REGULAR', 0, 0, 'WEBSITE', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'f', 'MYZRV229', NULL, NULL, NULL, NULL, NULL, '2025-06-06 13:27:34.512689', '2025-06-06 13:27:34.512689');
INSERT INTO "public"."customers" VALUES ('565a1d62-5cb2-462b-a7ea-1c3330d21e99', 'frontend@test.com', NULL, '前端测试用户', '', '13800138000', NULL, NULL, 'ACTIVE', 'REGULAR', 0, 0, 'WEBSITE', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'f', 'FZK5KDPJ', NULL, NULL, NULL, NULL, NULL, '2025-06-06 13:31:14.477951', '2025-06-06 13:31:14.477951');
INSERT INTO "public"."customers" VALUES ('0a17a999-aa53-4845-b02d-6629400ee38d', 'zhangsan@test.com', NULL, '张三测试', '', '13800138000', NULL, NULL, 'ACTIVE', 'REGULAR', 0, 0, 'WEBSITE', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'f', 'XOCS2VXP', NULL, NULL, NULL, NULL, NULL, '2025-06-06 13:37:55.539718', '2025-06-06 13:37:55.539718');
INSERT INTO "public"."customers" VALUES ('a3823bdf-b2b9-4ab5-9c0d-9b863ee5333c', 'ordertest@example.com', '$2b$12$mWYEuGjYD0HZ/ZATFK9dxe3EkeiCmPfAFZOeTNyVq.0HzPaySY5mC', 'Order', 'Test', NULL, NULL, NULL, 'ACTIVE', 'REGULAR', 0, 0, 'WEBSITE', NULL, '2025-06-06 14:04:27.822655', NULL, NULL, NULL, NULL, NULL, 'f', '5LJHX0UD', NULL, NULL, NULL, NULL, NULL, '2025-06-06 13:51:37.631552', '2025-06-06 14:04:27.824654');
INSERT INTO "public"."customers" VALUES ('6c78b575-cd35-414a-a400-d75b46677f2a', 'lijinyuan1983@outlook.com', '$2b$12$k3p5i9o20IVLc6Xc89iLK.Z44FgFTs0qlcUIaTzGwg5l4C2SKXD5S', NULL, NULL, NULL, NULL, NULL, 'ACTIVE', 'REGULAR', 0, 0, 'WEBSITE', NULL, '2025-06-06 20:38:35.106157', NULL, NULL, NULL, NULL, NULL, 't', '8ZTCJQX1', NULL, NULL, NULL, NULL, NULL, '2025-06-02 19:36:57.320584', '2025-06-06 20:38:35.106157');

-- ----------------------------
-- Table structure for data_backups
-- ----------------------------
DROP TABLE IF EXISTS "public"."data_backups";
CREATE TABLE "public"."data_backups" (
  "id" uuid NOT NULL,
  "backup_name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "backup_path" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "backup_size" int4,
  "backup_type" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "created_by" uuid,
  "created_at" timestamp(6) NOT NULL,
  "status" varchar(20) COLLATE "pg_catalog"."default",
  "notes" text COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "public"."data_backups"."backup_size" IS '备份文件大小，单位KB';
COMMENT ON COLUMN "public"."data_backups"."backup_type" IS '备份类型，如''full'', ''incremental''等';
COMMENT ON COLUMN "public"."data_backups"."status" IS '备份状态，如''in_progress'', ''completed'', ''failed''等';

-- ----------------------------
-- Records of data_backups
-- ----------------------------

-- ----------------------------
-- Table structure for email_verification_codes
-- ----------------------------
DROP TABLE IF EXISTS "public"."email_verification_codes";
CREATE TABLE "public"."email_verification_codes" (
  "id" uuid NOT NULL,
  "email" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "verification_code" varchar(6) COLLATE "pg_catalog"."default" NOT NULL,
  "purpose" varchar(20) COLLATE "pg_catalog"."default" NOT NULL,
  "is_used" bool,
  "used_at" timestamp(6),
  "expires_at" timestamp(6) NOT NULL,
  "ip_address" varchar(50) COLLATE "pg_catalog"."default",
  "user_agent" varchar(255) COLLATE "pg_catalog"."default",
  "attempts" int4,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."email_verification_codes"."email" IS '邮箱地址';
COMMENT ON COLUMN "public"."email_verification_codes"."verification_code" IS '6位验证码';
COMMENT ON COLUMN "public"."email_verification_codes"."purpose" IS '验证码用途：register, login, reset_password';
COMMENT ON COLUMN "public"."email_verification_codes"."is_used" IS '是否已使用';
COMMENT ON COLUMN "public"."email_verification_codes"."used_at" IS '使用时间';
COMMENT ON COLUMN "public"."email_verification_codes"."expires_at" IS '过期时间';
COMMENT ON COLUMN "public"."email_verification_codes"."ip_address" IS '请求IP地址';
COMMENT ON COLUMN "public"."email_verification_codes"."user_agent" IS '用户代理';
COMMENT ON COLUMN "public"."email_verification_codes"."attempts" IS '验证尝试次数';

-- ----------------------------
-- Records of email_verification_codes
-- ----------------------------
INSERT INTO "public"."email_verification_codes" VALUES ('27eb5fbd-13d1-4d4d-9a3b-373b7ca954e8', 'lijinyuan1983@outlook.com', '860919', 'register', 't', '2025-06-02 19:34:47.670235', '2025-06-02 19:43:17.171541', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 1, '2025-06-02 19:33:17.172539', '2025-06-02 19:34:47.672232');
INSERT INTO "public"."email_verification_codes" VALUES ('af756009-3807-4a9f-aabd-33774d379977', 'lijinyuan1983@outlook.com', '268450', 'register', 't', '2025-06-02 19:36:57.294808', '2025-06-02 19:46:14.795613', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 1, '2025-06-02 19:36:14.79762', '2025-06-02 19:36:57.29581');
INSERT INTO "public"."email_verification_codes" VALUES ('c7024561-4a1d-4a01-ab34-58a970d72e9a', 'lijinyuan1983@outlook.com', '934051', 'login', 't', '2025-06-02 19:40:04.396676', '2025-06-02 19:49:33.623568', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 1, '2025-06-02 19:39:33.625074', '2025-06-02 19:40:04.396676');
INSERT INTO "public"."email_verification_codes" VALUES ('526704d6-35f1-4d1c-8c8d-de2795f7f0d7', 'lijinyuan1983@outlook.com', '713599', 'login', 't', '2025-06-06 02:53:16.503006', '2025-06-06 03:02:53.039231', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 1, '2025-06-06 02:52:53.040232', '2025-06-06 02:53:16.504007');
INSERT INTO "public"."email_verification_codes" VALUES ('c20bdf52-aca4-4d39-8bb5-bbd86a1e23dd', 'lijinyuan1983@outlook.com', '920343', 'login', 't', '2025-06-06 03:01:49.914627', '2025-06-06 03:11:28.660227', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 1, '2025-06-06 03:01:28.660227', '2025-06-06 03:01:49.914627');
INSERT INTO "public"."email_verification_codes" VALUES ('79153afc-d67a-4986-8d48-9e9633287f21', 'lijinyuan1983@outlook.com', '562894', 'login', 'f', NULL, '2025-06-06 19:40:24.033082', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36', 0, '2025-06-06 19:30:24.035337', '2025-06-06 19:30:24.035337');
INSERT INTO "public"."email_verification_codes" VALUES ('086b067f-9b2d-4608-bd3e-17c8aaf858e9', 'lijinyuan1983@outlook.com', '521258', 'login', 'f', NULL, '2025-06-06 19:48:40.730688', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36', 3, '2025-06-06 19:38:40.730688', '2025-06-06 19:39:39.190939');
INSERT INTO "public"."email_verification_codes" VALUES ('62fd2052-9818-4431-96c9-3f9aac97850d', 'lijinyuan1983@outlook.com', '891273', 'login', 'f', NULL, '2025-06-06 19:53:46.211382', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36', 0, '2025-06-06 19:43:46.212381', '2025-06-06 19:43:46.212381');

-- ----------------------------
-- Table structure for gift_orders
-- ----------------------------
DROP TABLE IF EXISTS "public"."gift_orders";
CREATE TABLE "public"."gift_orders" (
  "id" uuid NOT NULL,
  "order_id" uuid NOT NULL,
  "sender_name" varchar(100) COLLATE "pg_catalog"."default",
  "sender_email" varchar(100) COLLATE "pg_catalog"."default",
  "sender_phone" varchar(30) COLLATE "pg_catalog"."default",
  "recipient_name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "recipient_email" varchar(100) COLLATE "pg_catalog"."default",
  "recipient_phone" varchar(30) COLLATE "pg_catalog"."default",
  "gift_message" text COLLATE "pg_catalog"."default",
  "is_gift_message_printed" bool,
  "is_price_hidden" bool,
  "gift_wrap_type" "public"."giftwraptype",
  "gift_wrap_color" varchar(50) COLLATE "pg_catalog"."default",
  "gift_wrap_note" text COLLATE "pg_catalog"."default",
  "gift_wrap_price" int4,
  "is_scheduled_delivery" bool,
  "scheduled_delivery_date" date,
  "scheduled_delivery_time_slot" varchar(50) COLLATE "pg_catalog"."default",
  "delivery_instructions" text COLLATE "pg_catalog"."default",
  "is_surprise" bool,
  "is_registry_order" bool,
  "registry_id" uuid,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."gift_orders"."sender_name" IS '送礼人姓名';
COMMENT ON COLUMN "public"."gift_orders"."sender_email" IS '送礼人邮箱';
COMMENT ON COLUMN "public"."gift_orders"."sender_phone" IS '送礼人电话';
COMMENT ON COLUMN "public"."gift_orders"."recipient_name" IS '收礼人姓名';
COMMENT ON COLUMN "public"."gift_orders"."recipient_email" IS '收礼人邮箱';
COMMENT ON COLUMN "public"."gift_orders"."recipient_phone" IS '收礼人电话';
COMMENT ON COLUMN "public"."gift_orders"."gift_message" IS '礼品留言';
COMMENT ON COLUMN "public"."gift_orders"."is_gift_message_printed" IS '是否打印礼品留言';
COMMENT ON COLUMN "public"."gift_orders"."is_price_hidden" IS '是否隐藏价格';
COMMENT ON COLUMN "public"."gift_orders"."gift_wrap_type" IS '礼品包装类型';
COMMENT ON COLUMN "public"."gift_orders"."gift_wrap_color" IS '礼品包装颜色';
COMMENT ON COLUMN "public"."gift_orders"."gift_wrap_note" IS '礼品包装备注';
COMMENT ON COLUMN "public"."gift_orders"."gift_wrap_price" IS '礼品包装价格';
COMMENT ON COLUMN "public"."gift_orders"."is_scheduled_delivery" IS '是否预约送达';
COMMENT ON COLUMN "public"."gift_orders"."scheduled_delivery_date" IS '预约送达日期';
COMMENT ON COLUMN "public"."gift_orders"."scheduled_delivery_time_slot" IS '预约送达时间段';
COMMENT ON COLUMN "public"."gift_orders"."delivery_instructions" IS '送达说明';
COMMENT ON COLUMN "public"."gift_orders"."is_surprise" IS '是否是惊喜';
COMMENT ON COLUMN "public"."gift_orders"."is_registry_order" IS '是否礼品登记订单';

-- ----------------------------
-- Records of gift_orders
-- ----------------------------

-- ----------------------------
-- Table structure for gift_registries
-- ----------------------------
DROP TABLE IF EXISTS "public"."gift_registries";
CREATE TABLE "public"."gift_registries" (
  "id" uuid NOT NULL,
  "customer_id" uuid NOT NULL,
  "title" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default",
  "registry_type" "public"."registrytype" NOT NULL,
  "status" "public"."registrystatus" NOT NULL,
  "event_date" date,
  "end_date" date,
  "is_public" bool,
  "access_code" varchar(20) COLLATE "pg_catalog"."default",
  "sharing_url" varchar(255) COLLATE "pg_catalog"."default",
  "message_to_guests" text COLLATE "pg_catalog"."default",
  "co_registrant_name" varchar(100) COLLATE "pg_catalog"."default",
  "shipping_address_id" uuid,
  "custom_theme" varchar(50) COLLATE "pg_catalog"."default",
  "thank_you_message_template" text COLLATE "pg_catalog"."default",
  "total_items" int4,
  "total_purchased" int4,
  "views_count" int4,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."gift_registries"."title" IS '登记标题';
COMMENT ON COLUMN "public"."gift_registries"."description" IS '登记描述';
COMMENT ON COLUMN "public"."gift_registries"."registry_type" IS '登记类型';
COMMENT ON COLUMN "public"."gift_registries"."status" IS '状态';
COMMENT ON COLUMN "public"."gift_registries"."event_date" IS '活动日期';
COMMENT ON COLUMN "public"."gift_registries"."end_date" IS '结束日期';
COMMENT ON COLUMN "public"."gift_registries"."is_public" IS '是否公开';
COMMENT ON COLUMN "public"."gift_registries"."access_code" IS '访问代码，用于非公开登记';
COMMENT ON COLUMN "public"."gift_registries"."sharing_url" IS '分享URL';
COMMENT ON COLUMN "public"."gift_registries"."message_to_guests" IS '给宾客的留言';
COMMENT ON COLUMN "public"."gift_registries"."co_registrant_name" IS '共同登记人姓名';
COMMENT ON COLUMN "public"."gift_registries"."custom_theme" IS '自定义主题';
COMMENT ON COLUMN "public"."gift_registries"."thank_you_message_template" IS '感谢信息模板';
COMMENT ON COLUMN "public"."gift_registries"."total_items" IS '总项目数';
COMMENT ON COLUMN "public"."gift_registries"."total_purchased" IS '已购买项目数';
COMMENT ON COLUMN "public"."gift_registries"."views_count" IS '查看次数';

-- ----------------------------
-- Records of gift_registries
-- ----------------------------

-- ----------------------------
-- Table structure for gift_registry_items
-- ----------------------------
DROP TABLE IF EXISTS "public"."gift_registry_items";
CREATE TABLE "public"."gift_registry_items" (
  "id" uuid NOT NULL,
  "registry_id" uuid NOT NULL,
  "product_id" uuid NOT NULL,
  "sku_id" uuid,
  "name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "sku_code" varchar(50) COLLATE "pg_catalog"."default",
  "image_url" varchar(255) COLLATE "pg_catalog"."default",
  "unit_price" numeric(10,2) NOT NULL,
  "desired_quantity" int4 NOT NULL,
  "purchased_quantity" int4,
  "remaining_quantity" int4,
  "priority" int4,
  "notes" text COLLATE "pg_catalog"."default",
  "is_active" bool,
  "is_private" bool,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."gift_registry_items"."name" IS '商品名称';
COMMENT ON COLUMN "public"."gift_registry_items"."sku_code" IS 'SKU编码';
COMMENT ON COLUMN "public"."gift_registry_items"."image_url" IS '商品图片URL';
COMMENT ON COLUMN "public"."gift_registry_items"."unit_price" IS '单价';
COMMENT ON COLUMN "public"."gift_registry_items"."desired_quantity" IS '期望数量';
COMMENT ON COLUMN "public"."gift_registry_items"."purchased_quantity" IS '已购买数量';
COMMENT ON COLUMN "public"."gift_registry_items"."remaining_quantity" IS '剩余数量';
COMMENT ON COLUMN "public"."gift_registry_items"."priority" IS '优先级，0-最高';
COMMENT ON COLUMN "public"."gift_registry_items"."notes" IS '备注';
COMMENT ON COLUMN "public"."gift_registry_items"."is_active" IS '是否激活';
COMMENT ON COLUMN "public"."gift_registry_items"."is_private" IS '是否私密，不显示给其他人';

-- ----------------------------
-- Records of gift_registry_items
-- ----------------------------

-- ----------------------------
-- Table structure for gift_registry_purchases
-- ----------------------------
DROP TABLE IF EXISTS "public"."gift_registry_purchases";
CREATE TABLE "public"."gift_registry_purchases" (
  "id" uuid NOT NULL,
  "registry_item_id" uuid NOT NULL,
  "order_id" uuid,
  "order_item_id" uuid,
  "purchaser_name" varchar(100) COLLATE "pg_catalog"."default",
  "purchaser_email" varchar(255) COLLATE "pg_catalog"."default",
  "quantity" int4 NOT NULL,
  "message" text COLLATE "pg_catalog"."default",
  "is_anonymous" bool,
  "status" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "is_thank_you_sent" bool,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."gift_registry_purchases"."purchaser_name" IS '购买人姓名';
COMMENT ON COLUMN "public"."gift_registry_purchases"."purchaser_email" IS '购买人邮箱';
COMMENT ON COLUMN "public"."gift_registry_purchases"."quantity" IS '购买数量';
COMMENT ON COLUMN "public"."gift_registry_purchases"."message" IS '留言';
COMMENT ON COLUMN "public"."gift_registry_purchases"."is_anonymous" IS '是否匿名购买';
COMMENT ON COLUMN "public"."gift_registry_purchases"."status" IS '状态：pending, fulfilled, cancelled';
COMMENT ON COLUMN "public"."gift_registry_purchases"."is_thank_you_sent" IS '是否已发送感谢信息';

-- ----------------------------
-- Records of gift_registry_purchases
-- ----------------------------

-- ----------------------------
-- Table structure for gift_wrappings
-- ----------------------------
DROP TABLE IF EXISTS "public"."gift_wrappings";
CREATE TABLE "public"."gift_wrappings" (
  "id" uuid NOT NULL,
  "code" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default",
  "is_active" bool,
  "price" float8 NOT NULL,
  "currency_code" varchar(3) COLLATE "pg_catalog"."default",
  "tax_class" varchar(50) COLLATE "pg_catalog"."default",
  "materials" text COLLATE "pg_catalog"."default",
  "color" varchar(50) COLLATE "pg_catalog"."default",
  "style" varchar(50) COLLATE "pg_catalog"."default",
  "occasions" varchar[] COLLATE "pg_catalog"."default",
  "primary_occasion" "public"."occasiontype",
  "weight" float8,
  "dimensions" json,
  "max_product_dimensions" json,
  "max_product_weight" float8,
  "image_url" varchar(255) COLLATE "pg_catalog"."default",
  "thumbnail_url" varchar(255) COLLATE "pg_catalog"."default",
  "preview_images" varchar[] COLLATE "pg_catalog"."default",
  "sort_order" int4,
  "allows_message" bool,
  "max_message_length" int4,
  "allows_card" bool,
  "available_cards" uuid[],
  "available_from" timestamp(6),
  "available_to" timestamp(6),
  "is_seasonal" bool,
  "limited_quantity" bool,
  "remaining_quantity" int4,
  "allowed_product_categories" uuid[],
  "excluded_products" uuid[],
  "allowed_countries" varchar[] COLLATE "pg_catalog"."default",
  "is_premium" bool,
  "is_default" bool,
  "is_free_above" float8,
  "preparation_time" int4,
  "requires_special_handling" bool,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."gift_wrappings"."code" IS '包装代码';
COMMENT ON COLUMN "public"."gift_wrappings"."name" IS '包装名称';
COMMENT ON COLUMN "public"."gift_wrappings"."description" IS '包装描述';
COMMENT ON COLUMN "public"."gift_wrappings"."is_active" IS '是否激活';
COMMENT ON COLUMN "public"."gift_wrappings"."price" IS '包装价格';
COMMENT ON COLUMN "public"."gift_wrappings"."currency_code" IS '货币代码';
COMMENT ON COLUMN "public"."gift_wrappings"."tax_class" IS '税费类别';
COMMENT ON COLUMN "public"."gift_wrappings"."materials" IS '包装材料描述';
COMMENT ON COLUMN "public"."gift_wrappings"."color" IS '颜色';
COMMENT ON COLUMN "public"."gift_wrappings"."style" IS '风格';
COMMENT ON COLUMN "public"."gift_wrappings"."occasions" IS '适用场合';
COMMENT ON COLUMN "public"."gift_wrappings"."primary_occasion" IS '主要适用场合';
COMMENT ON COLUMN "public"."gift_wrappings"."weight" IS '重量(克)';
COMMENT ON COLUMN "public"."gift_wrappings"."dimensions" IS '尺寸，如{length, width, height}格式';
COMMENT ON COLUMN "public"."gift_wrappings"."max_product_dimensions" IS '最大产品尺寸';
COMMENT ON COLUMN "public"."gift_wrappings"."max_product_weight" IS '最大产品重量(克)';
COMMENT ON COLUMN "public"."gift_wrappings"."image_url" IS '图片URL';
COMMENT ON COLUMN "public"."gift_wrappings"."thumbnail_url" IS '缩略图URL';
COMMENT ON COLUMN "public"."gift_wrappings"."preview_images" IS '预览图片URL列表';
COMMENT ON COLUMN "public"."gift_wrappings"."sort_order" IS '排序顺序';
COMMENT ON COLUMN "public"."gift_wrappings"."allows_message" IS '是否允许留言';
COMMENT ON COLUMN "public"."gift_wrappings"."max_message_length" IS '最大留言长度';
COMMENT ON COLUMN "public"."gift_wrappings"."allows_card" IS '是否允许添加卡片';
COMMENT ON COLUMN "public"."gift_wrappings"."available_cards" IS '可用卡片ID列表';
COMMENT ON COLUMN "public"."gift_wrappings"."available_from" IS '可用开始日期';
COMMENT ON COLUMN "public"."gift_wrappings"."available_to" IS '可用结束日期';
COMMENT ON COLUMN "public"."gift_wrappings"."is_seasonal" IS '是否季节性';
COMMENT ON COLUMN "public"."gift_wrappings"."limited_quantity" IS '是否限量';
COMMENT ON COLUMN "public"."gift_wrappings"."remaining_quantity" IS '剩余数量';
COMMENT ON COLUMN "public"."gift_wrappings"."allowed_product_categories" IS '允许的产品分类ID列表';
COMMENT ON COLUMN "public"."gift_wrappings"."excluded_products" IS '排除的产品ID列表';
COMMENT ON COLUMN "public"."gift_wrappings"."allowed_countries" IS '允许的国家代码列表';
COMMENT ON COLUMN "public"."gift_wrappings"."is_premium" IS '是否高级包装';
COMMENT ON COLUMN "public"."gift_wrappings"."is_default" IS '是否默认包装';
COMMENT ON COLUMN "public"."gift_wrappings"."is_free_above" IS '免费包装的订单金额阈值';
COMMENT ON COLUMN "public"."gift_wrappings"."preparation_time" IS '准备时间(分钟)';
COMMENT ON COLUMN "public"."gift_wrappings"."requires_special_handling" IS '是否需要特殊处理';

-- ----------------------------
-- Records of gift_wrappings
-- ----------------------------

-- ----------------------------
-- Table structure for installment_plans
-- ----------------------------
DROP TABLE IF EXISTS "public"."installment_plans";
CREATE TABLE "public"."installment_plans" (
  "id" uuid NOT NULL,
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "code" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default",
  "status" "public"."installmentplanstatus" NOT NULL,
  "number_of_installments" int4 NOT NULL,
  "installment_interval_days" int4,
  "min_down_payment_percentage" float8,
  "interest_rate" float8,
  "fee_fixed" float8,
  "fee_percentage" float8,
  "min_order_amount" float8,
  "max_order_amount" float8,
  "allowed_currencies" varchar[] COLLATE "pg_catalog"."default",
  "allowed_countries" varchar[] COLLATE "pg_catalog"."default",
  "payment_gateway_id" uuid,
  "gateway_plan_id" varchar(100) COLLATE "pg_catalog"."default",
  "allowed_customer_groups" uuid[],
  "min_customer_orders" int4,
  "requires_credit_check" bool,
  "allowed_product_categories" uuid[],
  "excluded_products" uuid[],
  "is_promotional" bool,
  "promotion_start_date" timestamp(6),
  "promotion_end_date" timestamp(6),
  "icon_url" varchar(255) COLLATE "pg_catalog"."default",
  "logo_url" varchar(255) COLLATE "pg_catalog"."default",
  "promotion_banner_url" varchar(255) COLLATE "pg_catalog"."default",
  "sort_order" int4,
  "ui_template" varchar(50) COLLATE "pg_catalog"."default",
  "payment_schedule_template" text COLLATE "pg_catalog"."default",
  "terms_and_conditions" text COLLATE "pg_catalog"."default",
  "meta_data" json,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."installment_plans"."name" IS '计划名称';
COMMENT ON COLUMN "public"."installment_plans"."code" IS '计划代码';
COMMENT ON COLUMN "public"."installment_plans"."description" IS '计划描述';
COMMENT ON COLUMN "public"."installment_plans"."status" IS '状态';
COMMENT ON COLUMN "public"."installment_plans"."number_of_installments" IS '分期数量';
COMMENT ON COLUMN "public"."installment_plans"."installment_interval_days" IS '分期间隔天数';
COMMENT ON COLUMN "public"."installment_plans"."min_down_payment_percentage" IS '最小首付百分比';
COMMENT ON COLUMN "public"."installment_plans"."interest_rate" IS '年利率';
COMMENT ON COLUMN "public"."installment_plans"."fee_fixed" IS '固定手续费';
COMMENT ON COLUMN "public"."installment_plans"."fee_percentage" IS '百分比手续费';
COMMENT ON COLUMN "public"."installment_plans"."min_order_amount" IS '最小订单金额';
COMMENT ON COLUMN "public"."installment_plans"."max_order_amount" IS '最大订单金额';
COMMENT ON COLUMN "public"."installment_plans"."allowed_currencies" IS '允许的货币代码列表';
COMMENT ON COLUMN "public"."installment_plans"."allowed_countries" IS '允许的国家代码列表';
COMMENT ON COLUMN "public"."installment_plans"."gateway_plan_id" IS '网关端计划ID';
COMMENT ON COLUMN "public"."installment_plans"."allowed_customer_groups" IS '允许的客户组ID列表';
COMMENT ON COLUMN "public"."installment_plans"."min_customer_orders" IS '客户最小历史订单数';
COMMENT ON COLUMN "public"."installment_plans"."requires_credit_check" IS '是否需要信用检查';
COMMENT ON COLUMN "public"."installment_plans"."allowed_product_categories" IS '允许的产品分类ID列表';
COMMENT ON COLUMN "public"."installment_plans"."excluded_products" IS '排除的产品ID列表';
COMMENT ON COLUMN "public"."installment_plans"."is_promotional" IS '是否促销计划';
COMMENT ON COLUMN "public"."installment_plans"."promotion_start_date" IS '促销开始日期';
COMMENT ON COLUMN "public"."installment_plans"."promotion_end_date" IS '促销结束日期';
COMMENT ON COLUMN "public"."installment_plans"."icon_url" IS '图标URL';
COMMENT ON COLUMN "public"."installment_plans"."logo_url" IS 'Logo URL';
COMMENT ON COLUMN "public"."installment_plans"."promotion_banner_url" IS '促销横幅URL';
COMMENT ON COLUMN "public"."installment_plans"."sort_order" IS '排序顺序';
COMMENT ON COLUMN "public"."installment_plans"."ui_template" IS 'UI模板';
COMMENT ON COLUMN "public"."installment_plans"."payment_schedule_template" IS '还款计划模板';
COMMENT ON COLUMN "public"."installment_plans"."terms_and_conditions" IS '条款和条件';
COMMENT ON COLUMN "public"."installment_plans"."meta_data" IS '额外元数据';

-- ----------------------------
-- Records of installment_plans
-- ----------------------------

-- ----------------------------
-- Table structure for inventory_history
-- ----------------------------
DROP TABLE IF EXISTS "public"."inventory_history";
CREATE TABLE "public"."inventory_history" (
  "id" uuid NOT NULL,
  "inventory_id" uuid NOT NULL,
  "order_id" uuid,
  "operation" "public"."inventoryoperation" NOT NULL,
  "quantity" int4 NOT NULL,
  "previous_quantity" int4 NOT NULL,
  "current_quantity" int4 NOT NULL,
  "operator_id" uuid,
  "reference_number" varchar(50) COLLATE "pg_catalog"."default",
  "notes" text COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."inventory_history"."operation" IS '操作类型';
COMMENT ON COLUMN "public"."inventory_history"."quantity" IS '变更数量，正为增加，负为减少';
COMMENT ON COLUMN "public"."inventory_history"."previous_quantity" IS '变更前数量';
COMMENT ON COLUMN "public"."inventory_history"."current_quantity" IS '变更后数量';
COMMENT ON COLUMN "public"."inventory_history"."reference_number" IS '参考单号，如采购单、销售单';
COMMENT ON COLUMN "public"."inventory_history"."notes" IS '备注信息';

-- ----------------------------
-- Records of inventory_history
-- ----------------------------

-- ----------------------------
-- Table structure for login_logs
-- ----------------------------
DROP TABLE IF EXISTS "public"."login_logs";
CREATE TABLE "public"."login_logs" (
  "id" uuid NOT NULL,
  "user_id" uuid NOT NULL,
  "ip_address" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "user_agent" varchar(255) COLLATE "pg_catalog"."default",
  "device_type" varchar(50) COLLATE "pg_catalog"."default",
  "login_time" timestamp(6) NOT NULL,
  "login_status" bool,
  "status_message" varchar(200) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "public"."login_logs"."login_status" IS '登录是否成功';
COMMENT ON COLUMN "public"."login_logs"."status_message" IS '登录失败原因等';

-- ----------------------------
-- Records of login_logs
-- ----------------------------
INSERT INTO "public"."login_logs" VALUES ('fcb1e800-05d8-4ecd-b5a0-534f0055c3a2', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-23 10:21:19.369485', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('1632f250-0638-49d4-8d42-6281d8062c1c', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-23 10:21:21.552135', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('e30aa632-1e7f-446c-b700-17e406079027', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-23 10:23:39.939341', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('8471b9a6-e67a-48b6-8cc9-30475de44c67', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-23 10:27:58.828754', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('55973467-7be5-474e-b8c3-41eba11b5330', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-23 10:28:42.328404', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('a25594ea-e14c-45ce-97a8-6df15af67320', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-23 10:29:05.078317', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('3fb89273-0e8d-4212-a0a2-662e806cf1d6', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-23 10:30:14.67378', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('af2831af-c5b9-4e83-af92-971654cb02ca', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-23 10:31:25.492851', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('e6a203c0-ed11-4683-a058-f4cfdd16b3e0', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-23 15:17:09.43791', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('b84ee083-923f-4211-8cd1-c03a14cc6630', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-23 15:17:14.342618', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('4d7e0f98-2395-4732-b671-ae5800a7e459', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-23 15:17:23.217968', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('a5eb89a8-e1bf-48cf-be59-659b7ac07728', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-23 16:43:41.634312', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('597707f6-01b7-415b-b8da-66bef0ae9261', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-23 16:44:55.069945', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('b522cc0c-34a6-4256-bd54-5f9e3b430f9b', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-23 16:45:45.641123', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('3af1a69f-9103-4f67-b51b-a79b0c0ff751', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-26 06:12:06.448383', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('31a3caa6-2ab1-4947-9aa6-015315777c3e', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-26 06:17:28.531388', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('af970578-b72c-46da-8035-6db0b4e4b419', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-26 06:28:50.201469', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('975cf5ae-dda9-4fae-a744-292f855b8544', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-26 07:57:02.578592', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('d31cdba4-53f9-469c-8bce-d41e923ca5c0', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-26 07:57:15.212576', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('2f590aec-8661-4628-a847-e1b0a1c5bf46', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-26 07:57:16.62448', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('270b70d4-4dd8-4774-90e6-be2b5c8498ff', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-26 07:57:30.674782', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('407280a5-750a-48ca-937a-1461a1c36dba', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-26 07:59:10.845121', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('47c587ba-7ead-4537-908b-dd4bb7d2de29', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-26 08:00:19.661095', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('79494fd5-2315-4ca2-abd5-cc4833405283', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-26 08:00:21.241328', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('1366b82f-8291-48f9-9c4d-14a2da8e791d', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-26 08:10:42.224919', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('8d261233-9897-415c-80d3-9125fc95a721', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-26 08:19:19.960087', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('e63a8c46-566c-40dc-9ac5-c9ab6f6f693f', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-26 08:19:23.370866', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('4caeb1a1-4961-4f01-8e1c-1033afae9633', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-26 08:32:37.071232', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('eb95694f-ffb1-43be-ba85-e67653e3e612', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-26 08:37:22.756978', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('105a7f9e-041e-401d-809f-22a8cd48cd6c', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-27 19:15:25.950452', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('2a53dc96-202a-47f4-aa14-468277e4d16e', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-27 19:15:35.60996', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('e7795bf9-eecc-45c7-ab18-2563733153d2', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-27 19:15:49.681163', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('ccf058a7-52c8-4e5d-b3ca-311539dddd17', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-28 00:24:55.769561', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('26a72234-5597-4ec1-9650-7241ce349a17', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-28 00:25:00.857718', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('27518853-7aca-4d78-8645-6c60e82b07dd', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-28 00:25:07.855758', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('5ec5251e-cee4-4f84-a2f4-5281b6bc84c9', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-28 04:57:30.287565', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('598cbf5f-d7c6-46f0-8705-6250227381b3', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-28 04:57:36.381463', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('669f8f45-2ab0-43db-b164-bf91b06828ba', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-28 05:02:50.355551', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('f6ab42f7-abbd-4cab-97a8-91b9c77363ba', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-28 05:08:01.268264', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('80de085f-558e-460a-8f68-58383b326711', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-28 05:10:25.009471', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('2381b048-8555-42a6-a3a6-6e6d39b0c4b6', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-28 05:49:15.387895', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('c1c990e3-700f-49fb-981b-7533aabb3378', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-28 05:49:34.145515', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('15ad050d-8029-48ae-ac81-89d1d5e9189e', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-28 05:49:48.566345', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('cd07dcc1-fb0a-4bfd-8f43-61be890d61d2', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-28 06:01:34.040773', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('dc8dc1c0-5c89-4cb1-8ad5-c2988aa77799', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-28 07:46:23.942109', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('54e40bf8-8c70-4081-bf7c-803a2335744c', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-28 07:46:30.709042', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('1cdef185-37be-4062-8442-26d143cff344', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-28 07:56:52.23144', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('19712dbb-4a19-4034-a4d2-0be0d9eae5d9', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-28 07:57:23.976002', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('1f502b97-549d-4294-a94a-c0eb6acbb5c5', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-28 08:08:01.606355', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('e65a749d-eb5c-43bc-b96f-b12feb0dcaf6', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-28 08:08:10.780795', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('f5ed15d6-fa68-4b60-9453-b8094ebe8d4f', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-28 08:08:15.292122', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('48b6f3ad-2bb1-4869-9e13-174a4eaacf0b', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-28 08:15:15.616424', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('8980d8ba-dae8-4163-b48a-117947231694', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-28 08:23:09.178703', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('ae713883-2a16-437c-9b0a-89dcbb02bd61', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-29 07:24:23.234344', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('f2bd2c12-4a58-4c42-9131-9ed3dfb3d5ac', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-29 07:24:29.209754', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('3450718c-d8c6-4cfc-8cf6-cd9766d5b029', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-29 09:49:45.262775', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('6126513f-773a-4de8-818f-81f5e0b3a604', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-29 11:54:19.73504', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('b5b7677a-54a1-41cd-8817-1d0ad5cbadd0', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-30 04:04:11.151552', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('f737dfef-4a00-4985-8d08-0ea832ef7a4f', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-30 05:13:32.403055', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('8a3d1f2c-d279-42a3-aed3-8dacdf3277ec', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-30 05:13:36.024253', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('ba98140a-14a4-4c76-8dda-dcd127ccbb26', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-30 07:50:31.060903', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('bc64efbd-9a45-4f82-85a7-9dbd4736debe', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-30 07:50:32.888346', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('410d7aeb-076a-49d4-9ad8-f96331edbff2', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-05-30 11:11:12.138398', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('012da0dc-b697-4611-a773-11277f26afe8', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-06-05 22:54:27.2443', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('afac52b3-cb8e-4723-b10b-850a86d70daa', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-06-05 22:55:25.892492', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('3971bdb8-07ef-4b27-9b0b-53f27a1a3b47', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-06-05 22:59:01.529772', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('84527770-b356-4dfe-aed3-850ee815a4df', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-06-05 23:15:16.858539', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('2b46cb42-1511-4454-bf2f-ea8f48a5b84e', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-06-05 23:15:22.093128', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('0088c2cf-0a18-4a60-b4f7-c524dbee378d', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'python-requests/2.32.3', 'desktop', '2025-06-06 00:42:30.617442', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('b963be48-ba85-4548-809f-584c68132f7f', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'python-requests/2.32.3', 'desktop', '2025-06-06 00:43:10.85446', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('6b81c33e-87d6-4d8c-a058-8e16f55faaca', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-06-06 00:43:30.302107', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('3075deb1-024e-4c55-a7b3-653966c3af65', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'desktop', '2025-06-06 00:43:36.013199', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('c53789b7-2bb4-49af-86d2-50bad0394a9a', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36', 'desktop', '2025-06-06 21:11:49.785767', 'f', '密码错误');
INSERT INTO "public"."login_logs" VALUES ('83083017-1360-450e-b257-848f7cd89082', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36', 'desktop', '2025-06-06 21:12:03.365063', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('1b0d56e9-96a2-4335-a5d0-4ef6dd5bf61d', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36', 'desktop', '2025-06-06 21:14:33.825991', 'f', '密码错误');
INSERT INTO "public"."login_logs" VALUES ('3c831ff4-aa9c-4ed6-baf5-ac12e977d35e', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36', 'desktop', '2025-06-06 21:15:34.03909', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('19c66a27-2c68-484b-ae63-af8ca332b671', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36', 'desktop', '2025-06-06 21:17:02.222289', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('64997744-8d41-4719-bb6a-0d6b657d6c14', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36', 'desktop', '2025-06-06 21:17:05.915567', 't', NULL);
INSERT INTO "public"."login_logs" VALUES ('2e2187e7-a5d8-4097-bbf2-d2105ddbdbb6', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36', 'desktop', '2025-06-07 03:50:13.779961', 'f', '密码错误');
INSERT INTO "public"."login_logs" VALUES ('dfaa9ae6-16ed-44cc-ac56-870832d45e66', '4b743dd6-1847-437c-b784-783f44c1a400', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36', 'desktop', '2025-06-07 03:50:33.772882', 't', NULL);

-- ----------------------------
-- Table structure for operation_logs
-- ----------------------------
DROP TABLE IF EXISTS "public"."operation_logs";
CREATE TABLE "public"."operation_logs" (
  "id" uuid NOT NULL,
  "user_id" uuid NOT NULL,
  "operation_type" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "target_model" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "target_id" varchar(100) COLLATE "pg_catalog"."default",
  "details" text COLLATE "pg_catalog"."default",
  "ip_address" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "operation_time" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."operation_logs"."operation_type" IS '操作类型，如''create'', ''update'', ''delete''等';
COMMENT ON COLUMN "public"."operation_logs"."target_model" IS '操作的目标模型，如''product'', ''order''等';
COMMENT ON COLUMN "public"."operation_logs"."target_id" IS '操作的目标ID';
COMMENT ON COLUMN "public"."operation_logs"."details" IS '操作详细信息，通常是JSON格式';

-- ----------------------------
-- Records of operation_logs
-- ----------------------------

-- ----------------------------
-- Table structure for order_items
-- ----------------------------
DROP TABLE IF EXISTS "public"."order_items";
CREATE TABLE "public"."order_items" (
  "id" uuid NOT NULL DEFAULT gen_random_uuid(),
  "order_id" uuid NOT NULL,
  "product_id" uuid,
  "sku_id" uuid,
  "status" "public"."orderitemstatus" NOT NULL DEFAULT 'PENDING'::orderitemstatus,
  "name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "sku_code" varchar(50) COLLATE "pg_catalog"."default",
  "quantity" int4 NOT NULL DEFAULT 1,
  "unit_price" numeric(10,2) NOT NULL,
  "subtotal" numeric(10,2) NOT NULL,
  "discount_amount" numeric(10,2) NOT NULL DEFAULT 0,
  "tax_amount" numeric(10,2) NOT NULL DEFAULT 0,
  "final_price" numeric(10,2) NOT NULL,
  "weight" float8,
  "width" float8,
  "height" float8,
  "length" float8,
  "discount_type" varchar(50) COLLATE "pg_catalog"."default",
  "discount_percentage" float8,
  "coupon_code" varchar(50) COLLATE "pg_catalog"."default",
  "attributes" jsonb,
  "image_url" varchar(255) COLLATE "pg_catalog"."default",
  "confirmed_quantity" int4 DEFAULT 0,
  "shipped_quantity" int4 DEFAULT 0,
  "delivered_quantity" int4 DEFAULT 0,
  "returned_quantity" int4 DEFAULT 0,
  "cancelled_quantity" int4 DEFAULT 0,
  "is_shipped" bool DEFAULT false,
  "is_returned" bool DEFAULT false,
  "is_cancelled" bool DEFAULT false,
  "can_cancel" bool DEFAULT true,
  "can_return" bool DEFAULT true,
  "can_exchange" bool DEFAULT true,
  "options" jsonb,
  "note" text COLLATE "pg_catalog"."default",
  "cancel_reason" varchar(255) COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL DEFAULT now(),
  "updated_at" timestamp(6) NOT NULL DEFAULT now(),
  "confirmed_at" timestamp(6),
  "shipped_at" timestamp(6),
  "delivered_at" timestamp(6),
  "cancelled_at" timestamp(6)
)
;

-- ----------------------------
-- Records of order_items
-- ----------------------------
INSERT INTO "public"."order_items" VALUES ('23786690-f8f4-40a6-b379-41ef6f4171ff', '212c71c5-53fe-4f05-b397-df4ae85a4bf7', 'd14d5542-e951-4a5f-8ef8-68453651b013', 'ba7bceb5-813f-47bc-af8d-b9c34b8b9e61', 'PENDING', '测试商品', 'TEST001', 2, 99.99, 199.98, 0.00, 0.00, 199.98, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '{"size": "L", "color": "红色"}', 'https://example.com/image.jpg', 0, 0, 0, 0, 0, 'f', 'f', 'f', 't', 't', 't', NULL, NULL, NULL, '2025-06-06 12:37:20.8738', '2025-06-06 12:37:20.8738', NULL, NULL, NULL, NULL);
INSERT INTO "public"."order_items" VALUES ('fc011878-d850-4efc-a55f-5024f7bec467', 'c42bf067-144a-4ec0-8341-156b386c057b', '4ed2ac2e-70c9-4679-a445-4076bf406fcd', '55d21ca1-488e-49f1-adb7-727a491de7f8', 'PENDING', '???? (??1)', 'SL-0001-8mm_COPY_1', 1, 128.00, 128.00, 0.00, 0.00, 128.00, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '{"image": "http://localhost:8008/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/a6f221c6adf448859ca0f253add9f548_1748425530.webp", "sale_price": 128, "sku_options": "SL-0001-8mm_COPY_1", "max_quantity": 50, "currency_code": "USD", "regular_price": 150, "parsed_options": {"size": "SL-0001-8mm", "color": "1", "material": "COPY"}}', NULL, 0, 0, 0, 0, 0, 'f', 'f', 'f', 't', 't', 't', NULL, NULL, NULL, '2025-06-06 13:08:17.165265', '2025-06-06 13:08:17.165265', NULL, NULL, NULL, NULL);
INSERT INTO "public"."order_items" VALUES ('d4011a85-5c72-45ee-a6b1-cfd30d6d015c', 'c5bcbf80-e7f7-4520-b052-5b8c6f2a6e82', '4ed2ac2e-70c9-4679-a445-4076bf406fcd', '55d21ca1-488e-49f1-adb7-727a491de7f8', 'PENDING', '五花手链 (副本1)', 'SL-0001-8mm_COPY_1', 1, 128.00, 128.00, 0.00, 0.00, 128.00, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '{"image": "http://localhost:8008/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/a6f221c6adf448859ca0f253add9f548_1748425530.webp", "sale_price": 128, "sku_options": "SL-0001-8mm_COPY_1", "max_quantity": 50, "currency_code": "USD", "regular_price": 150, "parsed_options": {"size": "SL-0001-8mm", "color": "1", "material": "COPY"}}', NULL, 0, 0, 0, 0, 0, 'f', 'f', 'f', 't', 't', 't', NULL, NULL, NULL, '2025-06-06 13:10:54.204517', '2025-06-06 13:10:54.204517', NULL, NULL, NULL, NULL);
INSERT INTO "public"."order_items" VALUES ('0995501d-35c4-4d52-8337-902779b8ad8a', 'de10aa19-efda-4689-a840-ebc5dca074ee', '4ed2ac2e-70c9-4679-a445-4076bf406fcd', '55d21ca1-488e-49f1-adb7-727a491de7f8', 'PENDING', '五花手链 (副本1)', 'SL-0001-8mm_COPY_1', 1, 128.00, 128.00, 0.00, 0.00, 128.00, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '{"image": "http://localhost:8008/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/a6f221c6adf448859ca0f253add9f548_1748425530.webp", "sale_price": 128, "sku_options": "SL-0001-8mm_COPY_1", "max_quantity": 50, "currency_code": "USD", "regular_price": 150, "parsed_options": {"size": "SL-0001-8mm", "color": "1", "material": "COPY"}}', NULL, 0, 0, 0, 0, 0, 'f', 'f', 'f', 't', 't', 't', NULL, NULL, NULL, '2025-06-06 13:13:21.323229', '2025-06-06 13:13:21.323229', NULL, NULL, NULL, NULL);
INSERT INTO "public"."order_items" VALUES ('a7399f9a-7b6e-4ba1-88c5-255e3f8e41f8', 'a56a7d9b-f9ef-4aba-9bde-68ba16eda05c', '4ed2ac2e-70c9-4679-a445-4076bf406fcd', '55d21ca1-488e-49f1-adb7-727a491de7f8', 'PENDING', '五花手链 (副本1)', 'SL-0001-8mm_COPY_1', 1, 128.00, 128.00, 0.00, 0.00, 128.00, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '{"test": "data"}', NULL, 0, 0, 0, 0, 0, 'f', 'f', 'f', 't', 't', 't', NULL, NULL, NULL, '2025-06-06 13:16:32.890891', '2025-06-06 13:16:32.890891', NULL, NULL, NULL, NULL);
INSERT INTO "public"."order_items" VALUES ('1c77493f-bc62-4337-956a-8f396f53b942', '7cf9b86b-3495-4940-90f0-28304ba89559', '4ed2ac2e-70c9-4679-a445-4076bf406fcd', '55d21ca1-488e-49f1-adb7-727a491de7f8', 'PENDING', '五花手链 (副本1)', 'SL-0001-8mm_COPY_1', 1, 128.00, 128.00, 0.00, 0.00, 128.00, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '{"image": "http://localhost:8008/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/a6f221c6adf448859ca0f253add9f548_1748425530.webp", "sale_price": 128, "sku_options": "SL-0001-8mm_COPY_1", "max_quantity": 50, "currency_code": "USD", "regular_price": 150, "parsed_options": {"size": "SL-0001-8mm", "color": "1", "material": "COPY"}}', NULL, 0, 0, 0, 0, 0, 'f', 'f', 'f', 't', 't', 't', NULL, NULL, NULL, '2025-06-06 13:17:27.722333', '2025-06-06 13:17:27.722333', NULL, NULL, NULL, NULL);
INSERT INTO "public"."order_items" VALUES ('82e25f31-6cde-4458-b515-1a8a956ddd24', 'f9f73b6e-d277-4fc5-a237-27f4c2b89983', '4ed2ac2e-70c9-4679-a445-4076bf406fcd', '55d21ca1-488e-49f1-adb7-727a491de7f8', 'PENDING', '????', '??SKU', 1, 128.00, 128.00, 0.00, 0.00, 128.00, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '{"test": "data"}', NULL, 0, 0, 0, 0, 0, 'f', 'f', 'f', 't', 't', 't', NULL, NULL, NULL, '2025-06-06 13:19:52.928251', '2025-06-06 13:19:52.928251', NULL, NULL, NULL, NULL);
INSERT INTO "public"."order_items" VALUES ('0785545f-e72d-4a77-8259-4bd9c7344284', '01954432-5e4d-4553-a3ed-f6fcc362216e', '4ed2ac2e-70c9-4679-a445-4076bf406fcd', '55d21ca1-488e-49f1-adb7-727a491de7f8', 'PENDING', '紫水晶吊坠', '小号-银色', 2, 128.00, 256.00, 0.00, 0.00, 256.00, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '{"size": "小号", "color": "紫色", "material": "银色"}', NULL, 0, 0, 0, 0, 0, 'f', 'f', 'f', 't', 't', 't', NULL, NULL, NULL, '2025-06-06 13:21:03.748204', '2025-06-06 13:21:03.748204', NULL, NULL, NULL, NULL);
INSERT INTO "public"."order_items" VALUES ('3fc56535-ff89-4544-ba8a-5cb750d61a4b', '129105a7-a464-443c-a02a-39209cf3eff0', '4ed2ac2e-70c9-4679-a445-4076bf406fcd', '55d21ca1-488e-49f1-adb7-727a491de7f8', 'PENDING', '紫水晶吊坠', '小号-银色', 2, 128.00, 256.00, 0.00, 0.00, 256.00, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '{"size": "小号", "color": "紫色", "material": "银色"}', NULL, 0, 0, 0, 0, 0, 'f', 'f', 'f', 't', 't', 't', NULL, NULL, NULL, '2025-06-06 13:23:03.056307', '2025-06-06 13:23:03.056307', NULL, NULL, NULL, NULL);
INSERT INTO "public"."order_items" VALUES ('a62edcae-00ba-47bf-a942-3d6df3b7f2c2', '53d43d59-5ce4-42a3-a7ed-06adfeabf391', '4ed2ac2e-70c9-4679-a445-4076bf406fcd', '55d21ca1-488e-49f1-adb7-727a491de7f8', 'PENDING', '?????', '??-??', 2, 128.00, 256.00, 0.00, 0.00, 256.00, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '{"size": "??", "color": "??", "material": "??"}', NULL, 0, 0, 0, 0, 0, 'f', 'f', 'f', 't', 't', 't', NULL, NULL, NULL, '2025-06-06 13:23:36.67326', '2025-06-06 13:23:36.67326', NULL, NULL, NULL, NULL);
INSERT INTO "public"."order_items" VALUES ('0a675802-f638-4dc9-948b-76836fb9a3ec', 'ad1cf66b-86e0-4636-a062-b5e893fc27fe', '4ed2ac2e-70c9-4679-a445-4076bf406fcd', '55d21ca1-488e-49f1-adb7-727a491de7f8', 'PENDING', '紫水晶吊坠', '小号-银色', 2, 128.00, 256.00, 0.00, 0.00, 256.00, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '{"size": "小号", "color": "紫色", "material": "银色"}', NULL, 0, 0, 0, 0, 0, 'f', 'f', 'f', 't', 't', 't', NULL, NULL, NULL, '2025-06-06 13:25:34.560642', '2025-06-06 13:25:34.560642', NULL, NULL, NULL, NULL);
INSERT INTO "public"."order_items" VALUES ('831245ef-d1e2-4eba-9e64-59afc5ef25c9', '17563b0e-ea73-47d4-ad7f-e2dc0d272ea3', '4ed2ac2e-70c9-4679-a445-4076bf406fcd', '55d21ca1-488e-49f1-adb7-727a491de7f8', 'PENDING', '?????', '??-??', 2, 128.00, 256.00, 0.00, 0.00, 256.00, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '{"size": "??", "color": "??", "material": "??"}', NULL, 0, 0, 0, 0, 0, 'f', 'f', 'f', 't', 't', 't', NULL, NULL, NULL, '2025-06-06 13:25:49.420073', '2025-06-06 13:25:49.420073', NULL, NULL, NULL, NULL);
INSERT INTO "public"."order_items" VALUES ('729e2c3b-136f-42b4-8405-44a2c6652991', 'e14a7118-c228-4897-aa39-c98c6c16fd0f', '4ed2ac2e-70c9-4679-a445-4076bf406fcd', '55d21ca1-488e-49f1-adb7-727a491de7f8', 'PENDING', '紫水晶吊坠', '小号-银色', 2, 128.00, 256.00, 0.00, 0.00, 256.00, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '{"size": "小号", "color": "紫色", "material": "银色"}', NULL, 0, 0, 0, 0, 0, 'f', 'f', 'f', 't', 't', 't', NULL, NULL, NULL, '2025-06-06 13:27:34.525996', '2025-06-06 13:27:34.525996', NULL, NULL, NULL, NULL);
INSERT INTO "public"."order_items" VALUES ('87d46f2e-ec94-4749-a7ab-2769fd07f61d', 'e14a7118-c228-4897-aa39-c98c6c16fd0f', '4ed2ac2e-70c9-4679-a445-4076bf406fcd', '55d21ca1-488e-49f1-adb7-727a491de7f8', 'PENDING', '月光石手链', '中号-玫瑰金', 1, 88.00, 88.00, 0.00, 0.00, 88.00, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '{"size": "中号", "color": "白色", "material": "玫瑰金"}', NULL, 0, 0, 0, 0, 0, 'f', 'f', 'f', 't', 't', 't', NULL, NULL, NULL, '2025-06-06 13:27:34.525996', '2025-06-06 13:27:34.525996', NULL, NULL, NULL, NULL);
INSERT INTO "public"."order_items" VALUES ('e712b75e-2a5b-4ae2-8160-f07aa0edab49', '0ebc6df0-ab36-4e9c-80b3-9a5508df769c', '4ed2ac2e-70c9-4679-a445-4076bf406fcd', '55d21ca1-488e-49f1-adb7-727a491de7f8', 'PENDING', '测试商品-前端展示', '测试SKU', 1, 199.00, 199.00, 0.00, 0.00, 199.00, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '{"test": "frontend"}', NULL, 0, 0, 0, 0, 0, 'f', 'f', 'f', 't', 't', 't', NULL, NULL, NULL, '2025-06-06 13:31:14.491485', '2025-06-06 13:31:14.491485', NULL, NULL, NULL, NULL);
INSERT INTO "public"."order_items" VALUES ('7ff57e7b-ae83-47be-98f6-ef757539aa3d', 'd77de28f-5308-4e78-b9b4-642fd8152f3e', '4ed2ac2e-70c9-4679-a445-4076bf406fcd', '55d21ca1-488e-49f1-adb7-727a491de7f8', 'PENDING', '最终测试商品', '测试规格', 3, 299.00, 897.00, 0.00, 0.00, 897.00, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '{"size": "大号", "color": "紫色"}', NULL, 0, 0, 0, 0, 0, 'f', 'f', 'f', 't', 't', 't', NULL, NULL, NULL, '2025-06-06 13:37:55.542911', '2025-06-06 13:37:55.542911', NULL, NULL, NULL, NULL);
INSERT INTO "public"."order_items" VALUES ('6a390749-831c-4894-bc25-d4966834d684', 'ea314056-c63e-44a0-8915-7016b2d664b9', '4ed2ac2e-70c9-4679-a445-4076bf406fcd', '55d21ca1-488e-49f1-adb7-727a491de7f8', 'PENDING', '最终测试商品', '测试规格', 3, 299.00, 897.00, 0.00, 0.00, 897.00, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '{"size": "大号", "color": "紫色"}', NULL, 0, 0, 0, 0, 0, 'f', 'f', 'f', 't', 't', 't', NULL, NULL, NULL, '2025-06-06 13:40:09.252765', '2025-06-06 13:40:09.252765', NULL, NULL, NULL, NULL);
INSERT INTO "public"."order_items" VALUES ('4ce2745c-42f7-4241-9812-5287b6f8b5c0', '43ed645b-6098-460b-a43b-7228d82d7475', '4ed2ac2e-70c9-4679-a445-4076bf406fcd', '55d21ca1-488e-49f1-adb7-727a491de7f8', 'PENDING', '用户测试商品', '测试规格', 2, 199.00, 398.00, 0.00, 0.00, 398.00, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '{"size": "中号", "color": "蓝色"}', NULL, 0, 0, 0, 0, 0, 'f', 'f', 'f', 't', 't', 't', NULL, NULL, NULL, '2025-06-06 13:51:45.531456', '2025-06-06 13:51:45.531456', NULL, NULL, NULL, NULL);

-- ----------------------------
-- Table structure for order_returns
-- ----------------------------
DROP TABLE IF EXISTS "public"."order_returns";
CREATE TABLE "public"."order_returns" (
  "id" uuid NOT NULL,
  "order_id" uuid NOT NULL,
  "return_number" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "status" "public"."returnstatus" NOT NULL,
  "reason" "public"."returnreason" NOT NULL,
  "reason_detail" text COLLATE "pg_catalog"."default",
  "requested_action" "public"."returnaction" NOT NULL,
  "approved_action" "public"."returnaction",
  "refund_amount" numeric(10,2),
  "refund_tax" numeric(10,2),
  "refund_shipping" numeric(10,2),
  "refund_total" numeric(10,2),
  "refund_method" varchar(50) COLLATE "pg_catalog"."default",
  "refund_transaction_id" varchar(100) COLLATE "pg_catalog"."default",
  "return_shipping_method" varchar(100) COLLATE "pg_catalog"."default",
  "return_tracking_number" varchar(100) COLLATE "pg_catalog"."default",
  "return_label_url" varchar(255) COLLATE "pg_catalog"."default",
  "customer_needs_to_ship" bool,
  "images" json,
  "attachments" json,
  "handler_id" uuid,
  "handler_name" varchar(100) COLLATE "pg_catalog"."default",
  "resolution_comment" text COLLATE "pg_catalog"."default",
  "customer_comment" text COLLATE "pg_catalog"."default",
  "admin_comment" text COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL,
  "approved_at" timestamp(6),
  "received_at" timestamp(6),
  "refunded_at" timestamp(6),
  "completed_at" timestamp(6)
)
;
COMMENT ON COLUMN "public"."order_returns"."return_number" IS '退货单号';
COMMENT ON COLUMN "public"."order_returns"."status" IS '退货状态';
COMMENT ON COLUMN "public"."order_returns"."reason" IS '退货原因';
COMMENT ON COLUMN "public"."order_returns"."reason_detail" IS '退货原因详情';
COMMENT ON COLUMN "public"."order_returns"."requested_action" IS '请求的处理方式';
COMMENT ON COLUMN "public"."order_returns"."approved_action" IS '批准的处理方式';
COMMENT ON COLUMN "public"."order_returns"."refund_amount" IS '退款金额';
COMMENT ON COLUMN "public"."order_returns"."refund_tax" IS '退款税费';
COMMENT ON COLUMN "public"."order_returns"."refund_shipping" IS '退款运费';
COMMENT ON COLUMN "public"."order_returns"."refund_total" IS '退款总额';
COMMENT ON COLUMN "public"."order_returns"."refund_method" IS '退款方式';
COMMENT ON COLUMN "public"."order_returns"."refund_transaction_id" IS '退款交易ID';
COMMENT ON COLUMN "public"."order_returns"."return_shipping_method" IS '退货物流方式';
COMMENT ON COLUMN "public"."order_returns"."return_tracking_number" IS '退货物流单号';
COMMENT ON COLUMN "public"."order_returns"."return_label_url" IS '退货标签URL';
COMMENT ON COLUMN "public"."order_returns"."customer_needs_to_ship" IS '客户是否需要返回商品';
COMMENT ON COLUMN "public"."order_returns"."images" IS '图片URL列表';
COMMENT ON COLUMN "public"."order_returns"."attachments" IS '附件URL列表';
COMMENT ON COLUMN "public"."order_returns"."handler_id" IS '处理人ID';
COMMENT ON COLUMN "public"."order_returns"."handler_name" IS '处理人姓名';
COMMENT ON COLUMN "public"."order_returns"."resolution_comment" IS '处理结果说明';
COMMENT ON COLUMN "public"."order_returns"."customer_comment" IS '客户备注';
COMMENT ON COLUMN "public"."order_returns"."admin_comment" IS '管理员备注';
COMMENT ON COLUMN "public"."order_returns"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."order_returns"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."order_returns"."approved_at" IS '批准时间';
COMMENT ON COLUMN "public"."order_returns"."received_at" IS '收到退货时间';
COMMENT ON COLUMN "public"."order_returns"."refunded_at" IS '退款时间';
COMMENT ON COLUMN "public"."order_returns"."completed_at" IS '完成时间';

-- ----------------------------
-- Records of order_returns
-- ----------------------------

-- ----------------------------
-- Table structure for order_shipments
-- ----------------------------
DROP TABLE IF EXISTS "public"."order_shipments";
CREATE TABLE "public"."order_shipments" (
  "id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "shipment_code" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "order_id" uuid NOT NULL,
  "status" "public"."shipmentstatus" NOT NULL DEFAULT 'PENDING'::shipmentstatus,
  "carrier_name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "tracking_number" varchar(100) COLLATE "pg_catalog"."default",
  "shipping_method" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "recipient_name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "recipient_phone" varchar(30) COLLATE "pg_catalog"."default" NOT NULL,
  "recipient_email" varchar(100) COLLATE "pg_catalog"."default",
  "shipping_address1" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "shipping_city" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "shipping_country" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "shipping_postcode" varchar(20) COLLATE "pg_catalog"."default" NOT NULL,
  "weight" float8 NOT NULL,
  "shipping_cost" numeric(10,2) NOT NULL DEFAULT 0,
  "estimated_delivery_date" timestamp(6),
  "notes" text COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "shipped_at" timestamp(6),
  "delivered_at" timestamp(6)
)
;

-- ----------------------------
-- Records of order_shipments
-- ----------------------------

-- ----------------------------
-- Table structure for orders
-- ----------------------------
DROP TABLE IF EXISTS "public"."orders";
CREATE TABLE "public"."orders" (
  "id" uuid NOT NULL DEFAULT gen_random_uuid(),
  "order_number" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "customer_id" uuid,
  "status" "public"."orderstatus" NOT NULL DEFAULT 'PENDING'::orderstatus,
  "payment_status" "public"."paymentstatus" NOT NULL DEFAULT 'PENDING'::paymentstatus,
  "shipping_status" "public"."shippingstatus" NOT NULL DEFAULT 'PENDING'::shippingstatus,
  "currency_code" varchar(3) COLLATE "pg_catalog"."default" NOT NULL,
  "subtotal" numeric(10,2) NOT NULL DEFAULT 0,
  "shipping_amount" numeric(10,2) NOT NULL DEFAULT 0,
  "tax_amount" numeric(10,2) NOT NULL DEFAULT 0,
  "discount_amount" numeric(10,2) NOT NULL DEFAULT 0,
  "total_amount" numeric(10,2) NOT NULL DEFAULT 0,
  "paid_amount" numeric(10,2) NOT NULL DEFAULT 0,
  "shipping_name" varchar(100) COLLATE "pg_catalog"."default",
  "shipping_phone" varchar(30) COLLATE "pg_catalog"."default",
  "shipping_email" varchar(100) COLLATE "pg_catalog"."default",
  "shipping_address1" varchar(255) COLLATE "pg_catalog"."default",
  "shipping_address2" varchar(255) COLLATE "pg_catalog"."default",
  "shipping_city" varchar(100) COLLATE "pg_catalog"."default",
  "shipping_state" varchar(100) COLLATE "pg_catalog"."default",
  "shipping_country" varchar(100) COLLATE "pg_catalog"."default",
  "shipping_postcode" varchar(20) COLLATE "pg_catalog"."default",
  "billing_name" varchar(100) COLLATE "pg_catalog"."default",
  "billing_phone" varchar(30) COLLATE "pg_catalog"."default",
  "billing_email" varchar(100) COLLATE "pg_catalog"."default",
  "billing_address1" varchar(255) COLLATE "pg_catalog"."default",
  "billing_address2" varchar(255) COLLATE "pg_catalog"."default",
  "billing_city" varchar(100) COLLATE "pg_catalog"."default",
  "billing_state" varchar(100) COLLATE "pg_catalog"."default",
  "billing_country" varchar(100) COLLATE "pg_catalog"."default",
  "billing_postcode" varchar(20) COLLATE "pg_catalog"."default",
  "coupon_code" varchar(50) COLLATE "pg_catalog"."default",
  "is_gift" bool DEFAULT false,
  "gift_message" text COLLATE "pg_catalog"."default",
  "customer_note" text COLLATE "pg_catalog"."default",
  "admin_note" text COLLATE "pg_catalog"."default",
  "ip_address" varchar(50) COLLATE "pg_catalog"."default",
  "user_agent" text COLLATE "pg_catalog"."default",
  "source" varchar(50) COLLATE "pg_catalog"."default",
  "estimate_delivery_date" timestamp(6),
  "created_at" timestamp(6) NOT NULL DEFAULT now(),
  "updated_at" timestamp(6) NOT NULL DEFAULT now(),
  "paid_at" timestamp(6),
  "shipped_at" timestamp(6),
  "delivered_at" timestamp(6),
  "completed_at" timestamp(6),
  "cancelled_at" timestamp(6)
)
;

-- ----------------------------
-- Records of orders
-- ----------------------------
INSERT INTO "public"."orders" VALUES ('212c71c5-53fe-4f05-b397-df4ae85a4bf7', '20250606189148', '9295ca8d-bcd8-4733-99e0-bc8646231f39', 'PENDING', 'PENDING', 'PENDING', 'CNY', 199.98, 10.00, 0.00, 0.00, 209.98, 0.00, '测试用户', '1234567890', 'test@example.com', '测试地址1', '测试地址2', '测试城市', '测试省份', '中国', '100000', '测试用户', '1234567890', 'test@example.com', '测试地址1', '测试地址2', '测试城市', '测试省份', '中国', '100000', NULL, 'f', NULL, '测试订单', NULL, '127.0.0.1', 'Test Agent', 'test', NULL, '2025-06-06 12:37:20.867799', '2025-06-06 12:37:20.867799', NULL, NULL, NULL, NULL, NULL);
INSERT INTO "public"."orders" VALUES ('de10aa19-efda-4689-a840-ebc5dca074ee', '20250606176403', 'd1619fc9-550c-4208-bf4b-5c4553ed99dd', 'PENDING', 'PENDING', 'PENDING', 'USD', 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 'Test User', '18180055588', 'test@example.com', 'test address', NULL, 'test city', 'test state', 'CN', '610010', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'f', NULL, 'Test order', NULL, '127.0.0.1', 'Test Agent', 'website', NULL, '2025-06-06 13:13:21.318233', '2025-06-06 13:13:21.318233', NULL, NULL, NULL, NULL, NULL);
INSERT INTO "public"."orders" VALUES ('a56a7d9b-f9ef-4aba-9bde-68ba16eda05c', '20250606339243', 'd1619fc9-550c-4208-bf4b-5c4553ed99dd', 'PENDING', 'PENDING', 'PENDING', 'USD', 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 'Test User', '18180055588', 'test@example.com', 'test address', NULL, 'test city', 'test state', 'CN', '610010', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'f', NULL, NULL, NULL, NULL, NULL, 'website', NULL, '2025-06-06 13:16:32.88738', '2025-06-06 13:16:32.88738', NULL, NULL, NULL, NULL, NULL);
INSERT INTO "public"."orders" VALUES ('f9f73b6e-d277-4fc5-a237-27f4c2b89983', '20250606499253', 'd1619fc9-550c-4208-bf4b-5c4553ed99dd', 'PENDING', 'PENDING', 'PENDING', 'USD', 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 'Test User', '18180055588', 'test@example.com', 'test address', NULL, 'test city', 'test state', 'CN', '610010', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'f', NULL, NULL, NULL, NULL, NULL, 'website', NULL, '2025-06-06 13:19:52.928251', '2025-06-06 13:19:52.928251', NULL, NULL, NULL, NULL, NULL);
INSERT INTO "public"."orders" VALUES ('01954432-5e4d-4553-a3ed-f6fcc362216e', '20250606575045', 'd1619fc9-550c-4208-bf4b-5c4553ed99dd', 'PENDING', 'PENDING', 'PENDING', 'USD', 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, '张三', '13800138000', 'test@example.com', '北京市朝阳区某某街道123号', 'A座1001室', '北京', '北京市', 'CN', '100000', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 't', '生日快乐！', '请小心包装', NULL, NULL, NULL, 'website', NULL, '2025-06-06 13:21:03.74716', '2025-06-06 13:21:03.74716', NULL, NULL, NULL, NULL, NULL);
INSERT INTO "public"."orders" VALUES ('129105a7-a464-443c-a02a-39209cf3eff0', '20250606782808', 'd1619fc9-550c-4208-bf4b-5c4553ed99dd', 'PENDING', 'PENDING', 'PENDING', 'USD', 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, '张三', '13800138000', 'test@example.com', '北京市朝阳区某某街道123号', 'A座1001室', '北京', '北京市', 'CN', '100000', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 't', '生日快乐！', '请小心包装', NULL, NULL, NULL, 'website', NULL, '2025-06-06 13:23:03.054054', '2025-06-06 13:23:03.054054', NULL, NULL, NULL, NULL, NULL);
INSERT INTO "public"."orders" VALUES ('53d43d59-5ce4-42a3-a7ed-06adfeabf391', '20250606783636', 'd1619fc9-550c-4208-bf4b-5c4553ed99dd', 'PENDING', 'PENDING', 'PENDING', 'USD', 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, '??', '13800138000', 'test@example.com', '??????????123?', 'A?1001?', '??', '???', 'CN', '100000', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 't', '????!', '?????', NULL, NULL, NULL, 'website', NULL, '2025-06-06 13:23:36.668785', '2025-06-06 13:23:36.668785', NULL, NULL, NULL, NULL, NULL);
INSERT INTO "public"."orders" VALUES ('ad1cf66b-86e0-4636-a062-b5e893fc27fe', '20250606907566', 'd1619fc9-550c-4208-bf4b-5c4553ed99dd', 'PENDING', 'PENDING', 'PENDING', 'USD', 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, '张三', '13800138000', 'test@example.com', '北京市朝阳区某某街道123号', 'A座1001室', '北京', '北京市', 'CN', '100000', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 't', '生日快乐！', '请小心包装', NULL, NULL, NULL, 'website', NULL, '2025-06-06 13:25:34.559645', '2025-06-06 13:25:34.559645', NULL, NULL, NULL, NULL, NULL);
INSERT INTO "public"."orders" VALUES ('17563b0e-ea73-47d4-ad7f-e2dc0d272ea3', '20250606866907', 'd1619fc9-550c-4208-bf4b-5c4553ed99dd', 'PENDING', 'PENDING', 'PENDING', 'USD', 256.00, 0.00, 0.00, 0.00, 256.00, 0.00, '??', '13800138000', 'test@example.com', '??????????123?', 'A?1001?', '??', '???', 'CN', '100000', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 't', '????!', '?????', NULL, NULL, NULL, 'website', NULL, '2025-06-06 13:25:49.418067', '2025-06-06 13:25:49.418067', NULL, NULL, NULL, NULL, NULL);
INSERT INTO "public"."orders" VALUES ('e14a7118-c228-4897-aa39-c98c6c16fd0f', '20250606480355', 'c39e8faa-1fb0-48fb-91a5-84a3c5920f35', 'PENDING', 'PENDING', 'PENDING', 'USD', 344.00, 15.00, 12.50, 5.00, 366.50, 0.00, '李小明', '13912345678', 'lixiaoming@example.com', '上海市浦东新区陆家嘴金融中心', 'B座2008室', '上海', '上海市', 'CN', '200120', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 't', '祝你生日快乐，愿你心想事成！', '请在工作日送达，谢谢！', NULL, NULL, NULL, 'website', NULL, '2025-06-06 13:27:34.524484', '2025-06-06 13:27:34.524484', NULL, NULL, NULL, NULL, NULL);
INSERT INTO "public"."orders" VALUES ('0ebc6df0-ab36-4e9c-80b3-9a5508df769c', '20250606960629', '565a1d62-5cb2-462b-a7ea-1c3330d21e99', 'PENDING', 'PENDING', 'PENDING', 'USD', 199.00, 0.00, 0.00, 0.00, 199.00, 0.00, '前端测试用户', '13800138000', 'frontend@test.com', '前端测试地址', NULL, '测试市', NULL, 'CN', '100000', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'f', NULL, NULL, NULL, NULL, NULL, 'website', NULL, '2025-06-06 13:31:14.489976', '2025-06-06 13:31:14.489976', NULL, NULL, NULL, NULL, NULL);
INSERT INTO "public"."orders" VALUES ('d77de28f-5308-4e78-b9b4-642fd8152f3e', '20250606923556', '0a17a999-aa53-4845-b02d-6629400ee38d', 'PENDING', 'PENDING', 'PENDING', 'USD', 897.00, 20.00, 15.00, 10.00, 922.00, 0.00, '张三测试', '13800138000', 'zhangsan@test.com', '北京市朝阳区测试街道123号', 'A座2008室', '北京', '北京市', 'CN', '100000', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 't', '这是一份特别的礼物！', '请小心包装，节日礼品', NULL, NULL, NULL, 'website', NULL, '2025-06-06 13:37:55.542392', '2025-06-06 13:37:55.542392', NULL, NULL, NULL, NULL, NULL);
INSERT INTO "public"."orders" VALUES ('ea314056-c63e-44a0-8915-7016b2d664b9', '20250606647559', '0a17a999-aa53-4845-b02d-6629400ee38d', 'PENDING', 'PENDING', 'PENDING', 'USD', 897.00, 20.00, 15.00, 10.00, 922.00, 0.00, '张三测试', '13800138000', 'zhangsan@test.com', '北京市朝阳区测试街道123号', 'A座2008室', '北京', '北京市', 'CN', '100000', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 't', '这是一份特别的礼物！', '请小心包装，节日礼品', NULL, NULL, NULL, 'website', NULL, '2025-06-06 13:40:09.249571', '2025-06-06 13:40:09.249571', NULL, NULL, NULL, NULL, NULL);
INSERT INTO "public"."orders" VALUES ('43ed645b-6098-460b-a43b-7228d82d7475', '20250606196616', 'a3823bdf-b2b9-4ab5-9c0d-9b863ee5333c', 'PENDING', 'PENDING', 'PENDING', 'USD', 398.00, 10.00, 8.00, 5.00, 411.00, 0.00, 'Order Test', '13900139000', 'ordertest@example.com', '测试地址123号', '', '测试市', '测试省', 'CN', '100001', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'f', NULL, '这是用户的测试订单', NULL, NULL, NULL, 'website', NULL, '2025-06-06 13:51:45.526512', '2025-06-06 13:51:45.526512', NULL, NULL, NULL, NULL, NULL);
INSERT INTO "public"."orders" VALUES ('c42bf067-144a-4ec0-8341-156b386c057b', '20250606933603', '6c78b575-cd35-414a-a400-d75b46677f2a', 'PENDING', 'PENDING', 'PENDING', 'USD', 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 'Jinyuan li', '18180055588', NULL, 'jiuxiangshifang 5-302', '', 'meishan', 'sichuan', 'CN', '610010', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'f', NULL, '', NULL, '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'website', NULL, '2025-06-06 13:08:17.161743', '2025-06-06 13:08:17.161743', NULL, NULL, NULL, NULL, NULL);
INSERT INTO "public"."orders" VALUES ('c5bcbf80-e7f7-4520-b052-5b8c6f2a6e82', '20250606724447', '6c78b575-cd35-414a-a400-d75b46677f2a', 'PENDING', 'PENDING', 'PENDING', 'USD', 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 'Jinyuan li', '18180055588', NULL, 'jiuxiangshifang 5-302', '', 'meishan', 'sichuan', 'CN', '610010', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'f', NULL, '', NULL, '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'website', NULL, '2025-06-06 13:10:54.202511', '2025-06-06 13:10:54.202511', NULL, NULL, NULL, NULL, NULL);
INSERT INTO "public"."orders" VALUES ('7cf9b86b-3495-4940-90f0-28304ba89559', '20250606526913', '6c78b575-cd35-414a-a400-d75b46677f2a', 'PENDING', 'PENDING', 'PENDING', 'USD', 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 'Jinyuan li', '18180055588', NULL, 'jiuxiangshifang 5-302', '', 'meishan', 'sichuan', 'CN', '610010', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'f', NULL, '', NULL, '', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0', 'website', NULL, '2025-06-06 13:17:27.719332', '2025-06-06 13:17:27.719332', NULL, NULL, NULL, NULL, NULL);

-- ----------------------------
-- Table structure for payment_gateways
-- ----------------------------
DROP TABLE IF EXISTS "public"."payment_gateways";
CREATE TABLE "public"."payment_gateways" (
  "id" uuid NOT NULL,
  "code" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default",
  "status" "public"."gatewaystatus" NOT NULL,
  "api_url" varchar(255) COLLATE "pg_catalog"."default",
  "sandbox_api_url" varchar(255) COLLATE "pg_catalog"."default",
  "api_key" varchar(255) COLLATE "pg_catalog"."default",
  "api_secret" varchar(255) COLLATE "pg_catalog"."default",
  "merchant_id" varchar(100) COLLATE "pg_catalog"."default",
  "webhook_url" varchar(255) COLLATE "pg_catalog"."default",
  "callback_url" varchar(255) COLLATE "pg_catalog"."default",
  "is_sandbox" bool,
  "encryption_key" varchar(255) COLLATE "pg_catalog"."default",
  "encryption_method" varchar(50) COLLATE "pg_catalog"."default",
  "signature_key" varchar(255) COLLATE "pg_catalog"."default",
  "supports_refund" bool,
  "supports_partial_refund" bool,
  "supports_installment" bool,
  "supports_recurring" bool,
  "supports_multi_currency" bool,
  "supported_currencies" json,
  "supported_countries" json,
  "settlement_currency" varchar(3) COLLATE "pg_catalog"."default",
  "settlement_period_days" int4,
  "logo_url" varchar(255) COLLATE "pg_catalog"."default",
  "icon_url" varchar(255) COLLATE "pg_catalog"."default",
  "config" json,
  "meta_data" json,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."payment_gateways"."code" IS '网关代码';
COMMENT ON COLUMN "public"."payment_gateways"."name" IS '网关名称';
COMMENT ON COLUMN "public"."payment_gateways"."description" IS '网关描述';
COMMENT ON COLUMN "public"."payment_gateways"."status" IS '状态';
COMMENT ON COLUMN "public"."payment_gateways"."api_url" IS 'API URL';
COMMENT ON COLUMN "public"."payment_gateways"."sandbox_api_url" IS '沙盒API URL';
COMMENT ON COLUMN "public"."payment_gateways"."api_key" IS 'API Key';
COMMENT ON COLUMN "public"."payment_gateways"."api_secret" IS 'API Secret';
COMMENT ON COLUMN "public"."payment_gateways"."merchant_id" IS '商户ID';
COMMENT ON COLUMN "public"."payment_gateways"."webhook_url" IS 'Webhook URL';
COMMENT ON COLUMN "public"."payment_gateways"."callback_url" IS '回调URL';
COMMENT ON COLUMN "public"."payment_gateways"."is_sandbox" IS '是否沙盒环境';
COMMENT ON COLUMN "public"."payment_gateways"."encryption_key" IS '加密密钥';
COMMENT ON COLUMN "public"."payment_gateways"."encryption_method" IS '加密方法';
COMMENT ON COLUMN "public"."payment_gateways"."signature_key" IS '签名密钥';
COMMENT ON COLUMN "public"."payment_gateways"."supports_refund" IS '是否支持退款';
COMMENT ON COLUMN "public"."payment_gateways"."supports_partial_refund" IS '是否支持部分退款';
COMMENT ON COLUMN "public"."payment_gateways"."supports_installment" IS '是否支持分期付款';
COMMENT ON COLUMN "public"."payment_gateways"."supports_recurring" IS '是否支持周期性付款';
COMMENT ON COLUMN "public"."payment_gateways"."supports_multi_currency" IS '是否支持多币种';
COMMENT ON COLUMN "public"."payment_gateways"."supported_currencies" IS '支持的货币';
COMMENT ON COLUMN "public"."payment_gateways"."supported_countries" IS '支持的国家/地区';
COMMENT ON COLUMN "public"."payment_gateways"."settlement_currency" IS '结算货币';
COMMENT ON COLUMN "public"."payment_gateways"."settlement_period_days" IS '结算周期(天)';
COMMENT ON COLUMN "public"."payment_gateways"."logo_url" IS 'Logo URL';
COMMENT ON COLUMN "public"."payment_gateways"."icon_url" IS '图标URL';
COMMENT ON COLUMN "public"."payment_gateways"."config" IS '额外配置信息';
COMMENT ON COLUMN "public"."payment_gateways"."meta_data" IS '元数据';

-- ----------------------------
-- Records of payment_gateways
-- ----------------------------

-- ----------------------------
-- Table structure for payment_logs
-- ----------------------------
DROP TABLE IF EXISTS "public"."payment_logs";
CREATE TABLE "public"."payment_logs" (
  "id" uuid NOT NULL,
  "transaction_id" uuid,
  "order_id" uuid,
  "user_id" uuid,
  "action" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "status" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "message" text COLLATE "pg_catalog"."default",
  "details" json,
  "ip_address" varchar(50) COLLATE "pg_catalog"."default",
  "user_agent" varchar(255) COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."payment_logs"."action" IS '操作类型';
COMMENT ON COLUMN "public"."payment_logs"."status" IS '操作状态';
COMMENT ON COLUMN "public"."payment_logs"."message" IS '日志消息';
COMMENT ON COLUMN "public"."payment_logs"."details" IS '详细信息';
COMMENT ON COLUMN "public"."payment_logs"."ip_address" IS 'IP地址';
COMMENT ON COLUMN "public"."payment_logs"."user_agent" IS 'User Agent';

-- ----------------------------
-- Records of payment_logs
-- ----------------------------

-- ----------------------------
-- Table structure for payment_methods
-- ----------------------------
DROP TABLE IF EXISTS "public"."payment_methods";
CREATE TABLE "public"."payment_methods" (
  "id" uuid NOT NULL,
  "code" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default",
  "instructions" text COLLATE "pg_catalog"."default",
  "status" "public"."paymentmethodstatus" NOT NULL,
  "fee_type" varchar(20) COLLATE "pg_catalog"."default",
  "fee_fixed" float8,
  "fee_percentage" float8,
  "min_fee" float8,
  "max_fee" float8,
  "icon_url" varchar(255) COLLATE "pg_catalog"."default",
  "logo_url" varchar(255) COLLATE "pg_catalog"."default",
  "sort_order" int4,
  "min_amount" float8,
  "max_amount" float8,
  "allowed_countries" json,
  "allowed_currencies" json,
  "gateway_id" uuid,
  "gateway_config" json,
  "is_default" bool,
  "is_cod" bool,
  "is_online" bool,
  "is_installment" bool,
  "is_public" bool,
  "meta_data" json,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."payment_methods"."code" IS '支付方式代码';
COMMENT ON COLUMN "public"."payment_methods"."name" IS '支付方式名称';
COMMENT ON COLUMN "public"."payment_methods"."description" IS '支付方式描述';
COMMENT ON COLUMN "public"."payment_methods"."instructions" IS '支付说明';
COMMENT ON COLUMN "public"."payment_methods"."status" IS '状态';
COMMENT ON COLUMN "public"."payment_methods"."fee_type" IS '手续费类型：fixed, percentage, mixed';
COMMENT ON COLUMN "public"."payment_methods"."fee_fixed" IS '固定手续费';
COMMENT ON COLUMN "public"."payment_methods"."fee_percentage" IS '百分比手续费';
COMMENT ON COLUMN "public"."payment_methods"."min_fee" IS '最低手续费';
COMMENT ON COLUMN "public"."payment_methods"."max_fee" IS '最高手续费';
COMMENT ON COLUMN "public"."payment_methods"."icon_url" IS '图标URL';
COMMENT ON COLUMN "public"."payment_methods"."logo_url" IS 'Logo URL';
COMMENT ON COLUMN "public"."payment_methods"."sort_order" IS '排序顺序';
COMMENT ON COLUMN "public"."payment_methods"."min_amount" IS '最小支付金额';
COMMENT ON COLUMN "public"."payment_methods"."max_amount" IS '最大支付金额';
COMMENT ON COLUMN "public"."payment_methods"."allowed_countries" IS '允许的国家/地区';
COMMENT ON COLUMN "public"."payment_methods"."allowed_currencies" IS '允许的货币';
COMMENT ON COLUMN "public"."payment_methods"."gateway_config" IS '支付网关配置';
COMMENT ON COLUMN "public"."payment_methods"."is_default" IS '是否默认支付方式';
COMMENT ON COLUMN "public"."payment_methods"."is_cod" IS '是否货到付款';
COMMENT ON COLUMN "public"."payment_methods"."is_online" IS '是否在线支付';
COMMENT ON COLUMN "public"."payment_methods"."is_installment" IS '是否支持分期';
COMMENT ON COLUMN "public"."payment_methods"."is_public" IS '是否公开显示';
COMMENT ON COLUMN "public"."payment_methods"."meta_data" IS '额外元数据';

-- ----------------------------
-- Records of payment_methods
-- ----------------------------

-- ----------------------------
-- Table structure for payment_statuses
-- ----------------------------
DROP TABLE IF EXISTS "public"."payment_statuses";
CREATE TABLE "public"."payment_statuses" (
  "id" uuid NOT NULL,
  "code" "public"."paymentstatusenum" NOT NULL,
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default",
  "color" varchar(20) COLLATE "pg_catalog"."default",
  "icon" varchar(50) COLLATE "pg_catalog"."default",
  "is_final" bool,
  "allowed_next_statuses" json,
  "requires_approval" bool,
  "triggers_action" varchar(50) COLLATE "pg_catalog"."default",
  "notify_customer" bool,
  "notify_admin" bool,
  "customer_message_template" text COLLATE "pg_catalog"."default",
  "admin_message_template" text COLLATE "pg_catalog"."default",
  "sort_order" int4,
  "is_system" bool,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."payment_statuses"."code" IS '状态代码';
COMMENT ON COLUMN "public"."payment_statuses"."name" IS '状态名称';
COMMENT ON COLUMN "public"."payment_statuses"."description" IS '状态描述';
COMMENT ON COLUMN "public"."payment_statuses"."color" IS '状态颜色代码';
COMMENT ON COLUMN "public"."payment_statuses"."icon" IS '状态图标';
COMMENT ON COLUMN "public"."payment_statuses"."is_final" IS '是否终态';
COMMENT ON COLUMN "public"."payment_statuses"."allowed_next_statuses" IS '允许的下一个状态';
COMMENT ON COLUMN "public"."payment_statuses"."requires_approval" IS '是否需要审批';
COMMENT ON COLUMN "public"."payment_statuses"."triggers_action" IS '触发的动作';
COMMENT ON COLUMN "public"."payment_statuses"."notify_customer" IS '是否通知客户';
COMMENT ON COLUMN "public"."payment_statuses"."notify_admin" IS '是否通知管理员';
COMMENT ON COLUMN "public"."payment_statuses"."customer_message_template" IS '客户通知模板';
COMMENT ON COLUMN "public"."payment_statuses"."admin_message_template" IS '管理员通知模板';
COMMENT ON COLUMN "public"."payment_statuses"."sort_order" IS '排序顺序';
COMMENT ON COLUMN "public"."payment_statuses"."is_system" IS '是否系统预设状态';

-- ----------------------------
-- Records of payment_statuses
-- ----------------------------

-- ----------------------------
-- Table structure for payment_transactions
-- ----------------------------
DROP TABLE IF EXISTS "public"."payment_transactions";
CREATE TABLE "public"."payment_transactions" (
  "id" uuid NOT NULL,
  "order_id" uuid,
  "payment_method_id" uuid NOT NULL,
  "transaction_type" "public"."transactiontype" NOT NULL,
  "status" "public"."transactionstatus" NOT NULL,
  "amount" float8 NOT NULL,
  "currency_code" varchar(3) COLLATE "pg_catalog"."default" NOT NULL,
  "fee_amount" float8,
  "transaction_id" varchar(100) COLLATE "pg_catalog"."default",
  "parent_transaction_id" uuid,
  "customer_id" uuid,
  "customer_ip" varchar(50) COLLATE "pg_catalog"."default",
  "customer_user_agent" varchar(255) COLLATE "pg_catalog"."default",
  "payment_details" json,
  "response_code" varchar(50) COLLATE "pg_catalog"."default",
  "response_message" text COLLATE "pg_catalog"."default",
  "gateway_response" json,
  "is_settled" bool,
  "settlement_date" timestamp(6),
  "description" text COLLATE "pg_catalog"."default",
  "note" text COLLATE "pg_catalog"."default",
  "meta_data" json,
  "refunded_amount" float8,
  "is_refundable" bool,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL,
  "expired_at" timestamp(6)
)
;
COMMENT ON COLUMN "public"."payment_transactions"."transaction_type" IS '交易类型';
COMMENT ON COLUMN "public"."payment_transactions"."status" IS '交易状态';
COMMENT ON COLUMN "public"."payment_transactions"."amount" IS '交易金额';
COMMENT ON COLUMN "public"."payment_transactions"."currency_code" IS '货币代码';
COMMENT ON COLUMN "public"."payment_transactions"."fee_amount" IS '手续费金额';
COMMENT ON COLUMN "public"."payment_transactions"."transaction_id" IS '第三方交易ID';
COMMENT ON COLUMN "public"."payment_transactions"."parent_transaction_id" IS '父交易ID';
COMMENT ON COLUMN "public"."payment_transactions"."customer_ip" IS '客户IP地址';
COMMENT ON COLUMN "public"."payment_transactions"."customer_user_agent" IS '客户User-Agent';
COMMENT ON COLUMN "public"."payment_transactions"."payment_details" IS '支付详情，如卡号后四位、支付账户等';
COMMENT ON COLUMN "public"."payment_transactions"."response_code" IS '响应代码';
COMMENT ON COLUMN "public"."payment_transactions"."response_message" IS '响应消息';
COMMENT ON COLUMN "public"."payment_transactions"."gateway_response" IS '网关响应详情';
COMMENT ON COLUMN "public"."payment_transactions"."is_settled" IS '是否已结算';
COMMENT ON COLUMN "public"."payment_transactions"."settlement_date" IS '结算日期';
COMMENT ON COLUMN "public"."payment_transactions"."description" IS '交易描述';
COMMENT ON COLUMN "public"."payment_transactions"."note" IS '内部备注';
COMMENT ON COLUMN "public"."payment_transactions"."meta_data" IS '元数据';
COMMENT ON COLUMN "public"."payment_transactions"."refunded_amount" IS '已退款金额';
COMMENT ON COLUMN "public"."payment_transactions"."is_refundable" IS '是否可退款';
COMMENT ON COLUMN "public"."payment_transactions"."expired_at" IS '过期时间';

-- ----------------------------
-- Records of payment_transactions
-- ----------------------------

-- ----------------------------
-- Table structure for permissions
-- ----------------------------
DROP TABLE IF EXISTS "public"."permissions";
CREATE TABLE "public"."permissions" (
  "id" uuid NOT NULL,
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "code" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "description" varchar(200) COLLATE "pg_catalog"."default",
  "module" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."permissions"."module" IS '权限所属模块，如''product'', ''order'', ''customer''等';

-- ----------------------------
-- Records of permissions
-- ----------------------------

-- ----------------------------
-- Table structure for product_attribute_values
-- ----------------------------
DROP TABLE IF EXISTS "public"."product_attribute_values";
CREATE TABLE "public"."product_attribute_values" (
  "id" uuid NOT NULL,
  "attribute_id" uuid NOT NULL,
  "value" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "label" varchar(255) COLLATE "pg_catalog"."default",
  "color_code" varchar(30) COLLATE "pg_catalog"."default",
  "image_url" varchar(255) COLLATE "pg_catalog"."default",
  "sort_order" int4,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."product_attribute_values"."value" IS '属性值';
COMMENT ON COLUMN "public"."product_attribute_values"."label" IS '显示标签';
COMMENT ON COLUMN "public"."product_attribute_values"."color_code" IS '颜色代码，当类型为颜色时使用';
COMMENT ON COLUMN "public"."product_attribute_values"."image_url" IS '图片URL，如颜色样式图';
COMMENT ON COLUMN "public"."product_attribute_values"."sort_order" IS '排序顺序';

-- ----------------------------
-- Records of product_attribute_values
-- ----------------------------
INSERT INTO "public"."product_attribute_values" VALUES ('332c402c-eb6f-410a-99d7-55c523ceaa12', '839db879-42aa-40fd-a0fa-663610c65521', '6mm', '6mm', NULL, NULL, 0, '2025-05-29 09:52:16.434278', '2025-05-29 09:52:16.434278');
INSERT INTO "public"."product_attribute_values" VALUES ('a14079b3-2acd-4168-b992-692304ae0cb4', '839db879-42aa-40fd-a0fa-663610c65521', '8mm', '8mm珠子直径', NULL, NULL, 1, '2025-05-29 10:12:10.249251', '2025-05-29 10:12:10.249251');
INSERT INTO "public"."product_attribute_values" VALUES ('50083ed7-8e4e-49a7-9859-9548458d6b09', '3d893608-44ba-4d7d-a711-4a07e60cb703', '白水晶', '白水晶', NULL, NULL, 0, '2025-05-30 05:32:58.259655', '2025-05-30 05:32:58.259655');
INSERT INTO "public"."product_attribute_values" VALUES ('31accb25-ec63-4574-8328-25674f8956d4', '3d893608-44ba-4d7d-a711-4a07e60cb703', '黑曜石', '黑曜石', NULL, NULL, 0, '2025-05-30 05:33:08.301077', '2025-05-30 05:33:08.301077');
INSERT INTO "public"."product_attribute_values" VALUES ('20a8eb98-b56e-4951-9182-e85e2be86619', '13225b54-0d5f-4e70-96f4-90ae93d38634', '红色', '鲜艳红色', NULL, NULL, 0, '2025-06-05 23:38:36.982068', '2025-06-05 23:38:36.982068');
INSERT INTO "public"."product_attribute_values" VALUES ('f8bd803a-7aa8-408c-97f4-983cc60c85dd', '13225b54-0d5f-4e70-96f4-90ae93d38634', '蓝色', '蓝色', NULL, NULL, 0, '2025-06-05 23:38:46.697455', '2025-06-05 23:38:46.697455');
INSERT INTO "public"."product_attribute_values" VALUES ('c51c747e-8bd9-4fe8-9d03-e6d9f9c5f36f', '13225b54-0d5f-4e70-96f4-90ae93d38634', '白色', '白色', NULL, NULL, 0, '2025-06-05 23:39:39.007451', '2025-06-05 23:39:39.007451');

-- ----------------------------
-- Table structure for product_attributes
-- ----------------------------
DROP TABLE IF EXISTS "public"."product_attributes";
CREATE TABLE "public"."product_attributes" (
  "id" uuid NOT NULL,
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "code" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default",
  "type" "public"."attributetype" NOT NULL,
  "display_order" int4,
  "is_required" bool,
  "is_configurable" bool,
  "is_searchable" bool,
  "is_comparable" bool,
  "is_filterable" bool,
  "is_visible_on_frontend" bool,
  "configuration" json,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."product_attributes"."name" IS '属性名称';
COMMENT ON COLUMN "public"."product_attributes"."code" IS '属性代码，如color, size';
COMMENT ON COLUMN "public"."product_attributes"."description" IS '属性描述';
COMMENT ON COLUMN "public"."product_attributes"."type" IS '属性类型';
COMMENT ON COLUMN "public"."product_attributes"."display_order" IS '显示顺序';
COMMENT ON COLUMN "public"."product_attributes"."is_required" IS '是否必填';
COMMENT ON COLUMN "public"."product_attributes"."is_configurable" IS '是否用于配置SKU的属性';
COMMENT ON COLUMN "public"."product_attributes"."is_searchable" IS '是否可搜索';
COMMENT ON COLUMN "public"."product_attributes"."is_comparable" IS '是否可比较';
COMMENT ON COLUMN "public"."product_attributes"."is_filterable" IS '是否可筛选';
COMMENT ON COLUMN "public"."product_attributes"."is_visible_on_frontend" IS '是否在前端可见';
COMMENT ON COLUMN "public"."product_attributes"."configuration" IS '属性配置信息，如验证规则';

-- ----------------------------
-- Records of product_attributes
-- ----------------------------
INSERT INTO "public"."product_attributes" VALUES ('839db879-42aa-40fd-a0fa-663610c65521', '珠子尺寸', 'bead_size', '手链或者项链的珠子的直径', 'SELECT', 0, 'f', 't', 'f', 'f', 't', 't', 'null', '2025-05-29 09:51:39.686688', '2025-05-29 09:51:39.686688');
INSERT INTO "public"."product_attributes" VALUES ('3d893608-44ba-4d7d-a711-4a07e60cb703', '玉石材料', 'jad_material', '饰品的玉石材料，比如：白水晶、黑曜石', 'SELECT', 0, 'f', 't', 'f', 'f', 't', 't', 'null', '2025-05-30 05:32:45.150554', '2025-05-30 05:32:45.150554');
INSERT INTO "public"."product_attributes" VALUES ('13225b54-0d5f-4e70-96f4-90ae93d38634', '颜色', 'color', '商品的主要颜色', 'SELECT', 0, 'f', 't', 'f', 'f', 't', 't', 'null', '2025-06-05 23:38:07.30977', '2025-06-05 23:38:07.30977');

-- ----------------------------
-- Table structure for product_bundles
-- ----------------------------
DROP TABLE IF EXISTS "public"."product_bundles";
CREATE TABLE "public"."product_bundles" (
  "id" uuid NOT NULL,
  "name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "slug" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default",
  "short_description" text COLLATE "pg_catalog"."default",
  "image_url" varchar(255) COLLATE "pg_catalog"."default",
  "sku_code" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "discount_type" varchar(20) COLLATE "pg_catalog"."default",
  "discount_value" float8,
  "is_active" bool,
  "is_featured" bool,
  "start_date" timestamp(6),
  "end_date" timestamp(6),
  "sort_order" int4,
  "seo_title" varchar(255) COLLATE "pg_catalog"."default",
  "seo_description" varchar(500) COLLATE "pg_catalog"."default",
  "seo_keywords" varchar(255) COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."product_bundles"."name" IS '套装名称';
COMMENT ON COLUMN "public"."product_bundles"."slug" IS '套装别名，用于URL';
COMMENT ON COLUMN "public"."product_bundles"."description" IS '套装描述';
COMMENT ON COLUMN "public"."product_bundles"."short_description" IS '简短描述';
COMMENT ON COLUMN "public"."product_bundles"."image_url" IS '套装主图URL';
COMMENT ON COLUMN "public"."product_bundles"."sku_code" IS '套装SKU编码';
COMMENT ON COLUMN "public"."product_bundles"."discount_type" IS '折扣类型：percentage, fixed_amount';
COMMENT ON COLUMN "public"."product_bundles"."discount_value" IS '折扣值';
COMMENT ON COLUMN "public"."product_bundles"."is_active" IS '是否激活';
COMMENT ON COLUMN "public"."product_bundles"."is_featured" IS '是否推荐套装';
COMMENT ON COLUMN "public"."product_bundles"."start_date" IS '套装开始日期';
COMMENT ON COLUMN "public"."product_bundles"."end_date" IS '套装结束日期';
COMMENT ON COLUMN "public"."product_bundles"."sort_order" IS '排序顺序';
COMMENT ON COLUMN "public"."product_bundles"."seo_title" IS 'SEO标题';
COMMENT ON COLUMN "public"."product_bundles"."seo_description" IS 'SEO描述';
COMMENT ON COLUMN "public"."product_bundles"."seo_keywords" IS 'SEO关键词';

-- ----------------------------
-- Records of product_bundles
-- ----------------------------

-- ----------------------------
-- Table structure for product_categories
-- ----------------------------
DROP TABLE IF EXISTS "public"."product_categories";
CREATE TABLE "public"."product_categories" (
  "id" uuid NOT NULL,
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "slug" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default",
  "parent_id" uuid,
  "level" "public"."categorylevel" NOT NULL,
  "image_url" varchar(255) COLLATE "pg_catalog"."default",
  "icon_url" varchar(255) COLLATE "pg_catalog"."default",
  "is_active" bool,
  "is_featured" bool,
  "sort_order" int4,
  "seo_title" varchar(255) COLLATE "pg_catalog"."default",
  "seo_description" varchar(500) COLLATE "pg_catalog"."default",
  "seo_keywords" varchar(255) COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."product_categories"."name" IS '分类名称';
COMMENT ON COLUMN "public"."product_categories"."slug" IS '分类别名，用于URL';
COMMENT ON COLUMN "public"."product_categories"."description" IS '分类描述';
COMMENT ON COLUMN "public"."product_categories"."parent_id" IS '父分类ID';
COMMENT ON COLUMN "public"."product_categories"."level" IS '分类层级';
COMMENT ON COLUMN "public"."product_categories"."image_url" IS '分类图片URL';
COMMENT ON COLUMN "public"."product_categories"."icon_url" IS '分类图标URL';
COMMENT ON COLUMN "public"."product_categories"."is_active" IS '是否激活';
COMMENT ON COLUMN "public"."product_categories"."is_featured" IS '是否推荐分类';
COMMENT ON COLUMN "public"."product_categories"."sort_order" IS '排序顺序';
COMMENT ON COLUMN "public"."product_categories"."seo_title" IS 'SEO标题';
COMMENT ON COLUMN "public"."product_categories"."seo_description" IS 'SEO描述';
COMMENT ON COLUMN "public"."product_categories"."seo_keywords" IS 'SEO关键词';

-- ----------------------------
-- Records of product_categories
-- ----------------------------
INSERT INTO "public"."product_categories" VALUES ('0b250eab-a67a-4d50-bdfc-2750efcd6142', '珠宝首饰', 'JEWELRY', '探索精美的珠宝首饰系列，包括项链、手链、戒指、耳环等多种饰品，每一件都经过精心设计，展现独特风格与卓越品质，是您表达个性与品味的理想选择。', NULL, 'LEVEL_1', NULL, NULL, 't', 'f', 0, '珠宝首饰 - 发现精美的珠宝饰品', '探索精美的珠宝首饰系列，包括项链、手链、戒指、耳环等。每一件饰品都经过精心设计，展现独特的风格与品味。我们提供多样化的选择，满足您不同的场合需求，是赠送自己或亲友的完美礼物。', '珠宝首饰, 精美饰品, 项链, 手链, 戒指, 耳环, 时尚配饰, 品质珠宝', '2025-05-28 03:00:22.429479', '2025-05-28 03:00:22.429479');
INSERT INTO "public"."product_categories" VALUES ('3c9af24e-e571-431a-bd5b-00f1d79b07cc', '目录', 'CATEGORIES', '珠宝首饰的分类目录，包含手链、项链与吊坠、戒指、耳环等多种类型，方便您根据喜好快速找到心仪的饰品。', '0b250eab-a67a-4d50-bdfc-2750efcd6142', 'LEVEL_2', NULL, NULL, 't', 'f', 10, '珠宝首饰分类目录 - 浏览各类饰品', '浏览珠宝首饰的完整分类目录，包括手链、项链、戒指、耳环等多种类型。每种类别都经过精心整理，帮助您快速找到符合个人风格的精美饰品，轻松搭配日常装扮或特殊场合穿着。', '珠宝分类, 饰品目录, 手链, 项链, 戒指, 耳环, 脚链, 发簪', '2025-05-28 03:00:22.430479', '2025-05-28 03:00:22.430479');
INSERT INTO "public"."product_categories" VALUES ('48744cc6-48df-48b4-9539-f8699185a13a', '手链', 'BRACELETS', '精选各类手链，从简约到华丽，展现个性与魅力。无论是单珠手链还是复杂编织款式，都能为您的腕间增添风采。', '3c9af24e-e571-431a-bd5b-00f1d79b07cc', 'LEVEL_3', NULL, NULL, 't', 'f', 100, '手链 - 精选各类个性手链', '探索精美的手链系列，从简约单珠到复杂编织，从金属材质到宝石镶嵌。每款手链都精心设计，展现独特风格，为您的腕间增添魅力，是日常搭配或礼物赠送的理想选择。', '手链, 个性手链, 珠宝手链, 编织手链, 宝石手链', '2025-05-28 03:00:22.431478', '2025-05-28 03:00:22.431478');
INSERT INTO "public"."product_categories" VALUES ('b1bcf436-aa43-41a7-9c22-79b2f990efff', '项链与吊坠', 'NECKLACES_PENDANTS', '优雅的项链与吊坠系列，从经典锁骨链到奢华多层次设计，点缀颈部风情，彰显高贵气质。', '3c9af24e-e571-431a-bd5b-00f1d79b07cc', 'LEVEL_3', NULL, NULL, 't', 'f', 110, '项链与吊坠 - 优雅颈部饰品', '发掘精美的项链与吊坠系列，包括经典锁骨链、吊坠项链、多层次设计等。每款作品都精心打造，展现优雅气质，为您的装扮增添亮点，是提升整体风格的必备单品。', '项链, 吊坠, 锁骨链, 珠宝项链, 时尚吊坠', '2025-05-28 03:00:22.432476', '2025-05-28 03:00:22.432476');
INSERT INTO "public"."product_categories" VALUES ('d93ed170-8f13-4e14-830c-4e616a23c355', '戒指', 'RINGS', '独特设计的戒指系列，从简约素圈到华丽宝石镶嵌，展现个性与品味，成为手指间的艺术表达。', '3c9af24e-e571-431a-bd5b-00f1d79b07cc', 'LEVEL_3', NULL, NULL, 't', 'f', 120, '戒指 - 独特设计指间饰品', '探索精美的戒指系列，从简约素圈到华丽宝石镶嵌，从传统款式到前卫设计。每枚戒指都精心制作，展现独特风格，是表达自我、纪念特殊时刻的理想选择。', '戒指, 宝石戒指, 设计师戒指, 婚戒, 时尚指环', '2025-05-28 03:00:22.43398', '2025-05-28 03:00:22.43398');
INSERT INTO "public"."product_categories" VALUES ('0781d07f-d69f-4149-8288-07d79041e0f1', '耳环', 'EARRINGS', '多样的耳环系列，从精致耳钉到摇曳耳坠，为您的耳畔增添光彩，成为整体造型的点睛之笔。', '3c9af24e-e571-431a-bd5b-00f1d79b07cc', 'LEVEL_3', NULL, NULL, 't', 'f', 130, '耳环 - 精致耳畔装饰', '浏览精美的耳环系列，包括耳钉、耳坠、耳环等多种类型。每款耳环都经过精心设计，展现不同风格，从日常简约到晚宴华丽，为您的耳畔增添光彩，提升整体造型魅力。', '耳环, 耳钉, 耳坠, 珠宝耳环, 时尚耳饰', '2025-05-28 03:00:22.434985', '2025-05-28 03:00:22.434985');
INSERT INTO "public"."product_categories" VALUES ('8e26b1a7-8d3a-4f57-b14c-07558036ae6c', '脚链', 'ANKLETS', '优雅的脚链系列，为足部增添精致装饰，展现女性的柔美与性感，是夏季海滩或特殊场合的理想配饰。', '3c9af24e-e571-431a-bd5b-00f1d79b07cc', 'LEVEL_3', NULL, NULL, 't', 'f', 140, '脚链 - 优雅足部装饰', '探索精美的脚链系列，从简约金属链到宝石镶嵌款式。每款脚链都精心设计，展现女性柔美与性感，是夏季海滩漫步或特殊场合的理想配饰，为您的整体造型增添独特魅力。', '脚链, 珠宝脚链, 装饰脚链, 夏季配饰', '2025-05-28 03:00:22.435985', '2025-05-28 03:00:22.435985');
INSERT INTO "public"."product_categories" VALUES ('7d18cc78-50b1-457f-a588-2694473582b1', '发簪', 'HAIRPIN', '传统与现代相结合的发簪系列，以精美的工艺和独特的设计，为您的发髻增添古典韵味与时尚感。', '3c9af24e-e571-431a-bd5b-00f1d79b07cc', 'LEVEL_3', NULL, NULL, 't', 'f', 150, '发簪 - 传统与现代的发饰艺术', '欣赏精美的发簪系列，融合传统工艺与现代设计。每支发簪都经过精心制作，展现古典韵味与时尚风格，为您的发髻增添独特魅力，是东方美学与现代审美完美结合的饰品。', '发簪, 传统发饰, 现代发簪, 东方饰品, 发饰', '2025-05-28 03:00:22.436986', '2025-05-28 03:00:22.436986');
INSERT INTO "public"."product_categories" VALUES ('b9f93620-7790-429d-9c94-25107f7d196c', '发梳', 'COMB', '精致的发梳系列，不仅实用且兼具装饰功能，以优雅的设计点缀发间，展现女性的温婉与优雅。', '3c9af24e-e571-431a-bd5b-00f1d79b07cc', 'LEVEL_3', NULL, NULL, 't', 'f', 160, '发梳 - 实用与装饰并存的发间饰品', '探索精美的发梳系列，兼具实用功能与装饰效果。每把发梳都经过精心设计，展现优雅风格，为您的发间增添亮点，是日常造型或特殊场合的理想配饰，展现女性的温婉与优雅气质。', '发梳, 装饰发梳, 女士发饰, 优雅发饰', '2025-05-28 03:00:22.436986', '2025-05-28 03:00:22.436986');
INSERT INTO "public"."product_categories" VALUES ('a2f37ca8-e1b1-4969-abb1-2af26e9ffc62', '胸针', 'BROOCH', '独特的胸针系列，以创意设计和精美工艺，为您的服装增添艺术气息，成为整体造型的亮点装饰。', '3c9af24e-e571-431a-bd5b-00f1d79b07cc', 'LEVEL_3', NULL, NULL, 't', 'f', 170, '胸针 - 创意服装装饰品', '浏览精美的胸针系列，从简约金属到宝石镶嵌，从传统图案到现代设计。每枚胸针都精心制作，展现独特风格，为您的服装增添艺术气息，是提升整体造型品质的理想配饰。', '胸针, 时尚胸针, 艺术胸针, 服装配饰', '2025-05-28 03:00:22.438491', '2025-05-28 03:00:22.438491');
INSERT INTO "public"."product_categories" VALUES ('e61707f0-a0ae-4662-a3b6-3e5354e0587f', '探索', 'EXPLORE', '特别策划的珠宝首饰探索系列，根据性别、年龄和特定款式分类，帮助您精准找到心仪的饰品。', '0b250eab-a67a-4d50-bdfc-2750efcd6142', 'LEVEL_2', NULL, NULL, 't', 'f', 20, '探索珠宝首饰 - 特别系列分类', '进入珠宝首饰的探索系列，根据性别、年龄和特定款式精心分类。无论是女士、男士还是儿童饰品，或是流行的红绳系列，都能帮助您快速找到符合需求的精美饰品，展现个性与风格。', '珠宝探索, 特别系列, 女士饰品, 男士饰品, 儿童饰品', '2025-05-28 03:00:22.439497', '2025-05-28 03:00:22.439497');
INSERT INTO "public"."product_categories" VALUES ('82300a7e-38a5-4ca7-9998-2b14812abf0c', '女士手链', 'WOMENS_BRACELETS', '专为女性设计的手链系列，融合优雅与时尚元素，展现女性的柔美与魅力，是日常搭配或礼物赠送的理想选择。', 'e61707f0-a0ae-4662-a3b6-3e5354e0587f', 'LEVEL_3', NULL, NULL, 't', 'f', 200, '女士手链 - 优雅与时尚的腕间饰品', '探索专为女性设计的手链系列，融合优雅与时尚元素。从简约金属到宝石镶嵌，从编织款式到金属链条，每款手链都精心打造，展现女性的柔美与魅力，是提升整体造型的完美配饰。', '女士手链, 女性饰品, 优雅手链, 时尚手链', '2025-05-28 03:00:22.440884', '2025-05-28 03:00:22.440884');
INSERT INTO "public"."product_categories" VALUES ('b7aeb673-102c-41d5-94f3-f2d05e0d4c81', '男士手链', 'MENS_BRACELETS', '专为男性打造的手链系列，以简约、大气的设计展现阳刚之气，是彰显个性与品味的腕间装饰。', 'e61707f0-a0ae-4662-a3b6-3e5354e0587f', 'LEVEL_3', NULL, NULL, 't', 'f', 210, '男士手链 - 简约大气的腕间装饰', '浏览专为男性设计的手链系列，以简约、大气的设计展现阳刚之气。从皮革编织到金属链条，从素色到镶嵌宝石，每款手链都精心制作，成为彰显个性与品味的理想配饰，适合各种场合佩戴。', '男士手链, 男性饰品, 阳刚手链, 个性手链', '2025-05-28 03:00:22.441891', '2025-05-28 03:00:22.441891');
INSERT INTO "public"."product_categories" VALUES ('60904db1-acc7-47ea-88eb-bbbe9db46162', '儿童手链', 'KIDS_BRACELET', '专为儿童设计的手链系列，以安全材质和可爱造型，为小朋友增添天真与活力，是成长纪念的理想礼物。', 'e61707f0-a0ae-4662-a3b6-3e5354e0587f', 'LEVEL_3', NULL, NULL, 't', 'f', 220, '儿童手链 - 安全可爱的童趣饰品', '探索专为儿童设计的手链系列，采用安全材质和可爱造型。从卡通形象到彩色珠子，从简约设计到趣味图案，每款手链都精心制作，为小朋友增添天真与活力，是记录成长时刻的理想礼物。', '儿童手链, 安全饰品, 可爱手链, 儿童礼物', '2025-05-28 03:00:22.442891', '2025-05-28 03:00:22.442891');
INSERT INTO "public"."product_categories" VALUES ('16264aae-052d-4479-be0c-fc0b2ef169aa', '红绳手链', 'RED_STRING_BRACELET', '流行的红绳手链系列，融合传统与时尚元素，以简约设计展现独特魅力，是招财纳福、表达祝福的热门饰品。', 'e61707f0-a0ae-4662-a3b6-3e5354e0587f', 'LEVEL_3', NULL, NULL, 't', 'f', 230, '红绳手链 - 传统与时尚的祝福饰品', '浏览流行的红绳手链系列，融合传统与时尚元素。从简约单绳到多股编织，从纯色红绳到搭配宝石珠子，每款手链都精心设计，展现独特魅力，是招财纳福、表达祝福的理想配饰。', '红绳手链, 招财饰品, 传统手链, 时尚红绳', '2025-05-28 03:00:22.442891', '2025-05-28 03:00:22.442891');
INSERT INTO "public"."product_categories" VALUES ('d8733286-c141-496c-8b55-0ef2710accd5', '红绳腰链', 'RED_STRING_BELLY_CHAIN', '独特的红绳腰链系列，以精致设计点缀腰部，展现女性的曲线美，为整体造型增添亮点与个性。', 'e61707f0-a0ae-4662-a3b6-3e5354e0587f', 'LEVEL_3', NULL, NULL, 't', 'f', 240, '红绳腰链 - 点缀腰部的时尚饰品', '探索独特的红绳腰链系列，以精致设计点缀腰部。从简约红绳到搭配宝石珠子，从传统编织到现代设计，每款腰链都精心制作，展现女性的曲线美，为整体造型增添亮点与个性，是时尚搭配的点睛之笔。', '红绳腰链, 女士腰链, 时尚腰饰, 红绳饰品', '2025-05-28 03:00:22.443891', '2025-05-28 03:00:22.443891');
INSERT INTO "public"."product_categories" VALUES ('f719f82c-39b4-4a61-8884-058aebea1c7f', '按宝石', 'BY_STONES', '根据珍贵宝石分类的珠宝首饰系列，从紫水晶到白水晶，每种宝石都蕴含独特能量与美丽光泽，为您的饰品增添特别意义。', '0b250eab-a67a-4d50-bdfc-2750efcd6142', 'LEVEL_2', NULL, NULL, 't', 'f', 30, '宝石珠宝首饰 - 探索不同宝石的魅力', '浏览根据珍贵宝石分类的珠宝首饰系列，从紫水晶到白水晶，每种宝石都蕴含独特能量与美丽光泽。我们精选优质宝石，精心制作成手链、项链、戒指等饰品，不仅展现时尚美感，更带来宝石的特别寓意，是您表达个性与追求美好的理想选择。', '宝石珠宝, 宝石手链, 宝石项链, 紫水晶, 绿松石, 白水晶', '2025-05-28 03:00:22.444891', '2025-05-28 03:00:22.444891');
INSERT INTO "public"."product_categories" VALUES ('e2041c77-4380-4b2a-93a6-f4dcf3ceb3b6', '紫水晶', 'AMETHYST', '紫水晶珠宝系列，以其迷人的紫色调和温和能量著称，象征平静与灵性，为佩戴者带来宁静与平衡。', 'f719f82c-39b4-4a61-8884-058aebea1c7f', 'LEVEL_3', NULL, NULL, 't', 'f', 300, '紫水晶珠宝 - 迷人紫色的能量饰品', '探索紫水晶珠宝系列，以其迷人的紫色调和温和能量著称。我们提供紫水晶手链、项链、戒指等多种款式，每件作品都精选优质紫水晶，精心制作而成。紫水晶象征平静与灵性，能为佩戴者带来宁静与平衡，是追求内心平静的理想配饰。', '紫水晶, 紫水晶珠宝, 紫色饰品, 能量宝石', '2025-05-28 03:00:22.444891', '2025-05-28 03:00:22.444891');
INSERT INTO "public"."product_categories" VALUES ('d8b08a2b-d034-4131-acb3-477277c6d82a', '绿松石', 'TURQUOISE', '绿松石珠宝系列，以其独特的蓝绿色和古老文化象征著称，代表幸运与保护，展现异域风情与自然之美。', 'f719f82c-39b4-4a61-8884-058aebea1c7f', 'LEVEL_3', NULL, NULL, 't', 'f', 310, '绿松石珠宝 - 蓝绿色的幸运保护符', '浏览绿松石珠宝系列，以其独特的蓝绿色和古老文化象征著称。我们提供绿松石手链、项链、戒指等多种款式，每件作品都精选优质绿松石，精心制作而成。绿松石代表幸运与保护，展现异域风情与自然之美，是追求独特风格与文化意义的理想配饰。', '绿松石, 绿松石珠宝, 蓝绿色饰品, 幸运宝石', '2025-05-28 03:00:22.44589', '2025-05-28 03:00:22.44589');
INSERT INTO "public"."product_categories" VALUES ('cad2a041-6eaf-4f39-bef4-2ade3a55d77d', '粉晶', 'ROSE_QUARTZ', '粉晶珠宝系列，以其柔和的粉红色调和爱心能量著称，象征爱与温柔，为佩戴者带来情感和谐与浪漫气息。', 'f719f82c-39b4-4a61-8884-058aebea1c7f', 'LEVEL_3', NULL, NULL, 't', 'f', 320, '粉晶珠宝 - 爱心能量的浪漫饰品', '探索粉晶珠宝系列，以其柔和的粉红色调和爱心能量著称。我们提供粉晶手链、项链、戒指等多种款式，每件作品都精选优质粉晶，精心制作而成。粉晶象征爱与温柔，能为佩戴者带来情感和谐与浪漫气息，是表达爱意与追求温柔的理想配饰。', '粉晶, 粉晶珠宝, 爱心宝石, 浪漫饰品', '2025-05-28 03:00:22.44589', '2025-05-28 03:00:22.44589');
INSERT INTO "public"."product_categories" VALUES ('b29c845c-07de-408d-94bf-fb682c9921f8', '月光石', 'MOONSTONE', '月光石珠宝系列，以其神秘的蓝白色泽和女性能量著称，象征直觉与情绪平衡，为佩戴者带来温柔的力量与内在和谐。', 'f719f82c-39b4-4a61-8884-058aebea1c7f', 'LEVEL_3', NULL, NULL, 't', 'f', 330, '月光石珠宝 - 神秘光泽的女性能量饰品', '浏览月光石珠宝系列，以其神秘的蓝白色泽和女性能量著称。我们提供月光石手链、项链、戒指等多种款式，每件作品都精选优质月光石，精心制作而成。月光石象征直觉与情绪平衡，能为佩戴者带来温柔的力量与内在和谐，是追求心灵平静与女性魅力的理想配饰。', '月光石, 月光石珠宝, 女性能量, 直觉宝石', '2025-05-28 03:00:22.44689', '2025-05-28 03:00:22.44689');
INSERT INTO "public"."product_categories" VALUES ('d739d9ce-3361-40f8-a0ca-c6e45af0b40f', '海蓝宝', 'AQUAMARINE', '海蓝宝珠宝系列，以其清新的蓝绿色和勇敢能量著称，象征勇气与清晰思维，为佩戴者带来自信与决策力。', 'f719f82c-39b4-4a61-8884-058aebea1c7f', 'LEVEL_3', NULL, NULL, 't', 'f', 340, '海蓝宝珠宝 - 清新蓝色的勇气饰品', '探索海蓝宝珠宝系列，以其清新的蓝绿色和勇敢能量著称。我们提供海蓝宝手链、项链、戒指等多种款式，每件作品都精选优质海蓝宝，精心制作而成。海蓝宝象征勇气与清晰思维，能为佩戴者带来自信与决策力，是追求突破与成长的理想配饰。', '海蓝宝, 海蓝宝珠宝, 勇气宝石, 蓝色饰品', '2025-05-28 03:00:22.447891', '2025-05-28 03:00:22.447891');
INSERT INTO "public"."product_categories" VALUES ('d5ff8b3b-ed80-484c-9d5f-12cf5273c94e', '翡翠', 'JADE', '翡翠珠宝系列，以其浓郁的绿色和东方文化象征著称，代表繁荣与长寿，展现高贵与典雅气质。', 'f719f82c-39b4-4a61-8884-058aebea1c7f', 'LEVEL_3', NULL, NULL, 't', 'f', 350, '翡翠珠宝 - 绿色贵族的东方魅力饰品', '浏览翡翠珠宝系列，以其浓郁的绿色和东方文化象征著称。我们提供翡翠手链、项链、戒指等多种款式，每件作品都精选优质翡翠，精心制作而成。翡翠代表繁荣与长寿，展现高贵与典雅气质，是传承东方文化与追求品质生活的理想配饰。', '翡翠, 翡翠珠宝, 东方文化, 绿色宝石', '2025-05-28 03:00:22.447891', '2025-05-28 03:00:22.447891');
INSERT INTO "public"."product_categories" VALUES ('846e749f-781f-4aff-8eff-0426b20d0de8', '孔雀石', 'MALACHITE', '孔雀石珠宝系列，以其独特的绿色条纹和保护能量著称，象征智慧与安全，为佩戴者带来守护与积极思维。', 'f719f82c-39b4-4a61-8884-058aebea1c7f', 'LEVEL_3', NULL, NULL, 't', 'f', 360, '孔雀石珠宝 - 绿色条纹的智慧保护符', '探索孔雀石珠宝系列，以其独特的绿色条纹和保护能量著称。我们提供孔雀石手链、项链、戒指等多种款式，每件作品都精选优质孔雀石，精心制作而成。孔雀石象征智慧与安全，能为佩戴者带来守护与积极思维，是追求身心保护与智慧启迪的理想配饰。', '孔雀石, 孔雀石珠宝, 保护宝石, 智慧饰品', '2025-05-28 03:00:22.44919', '2025-05-28 03:00:22.44919');
INSERT INTO "public"."product_categories" VALUES ('9e968995-d903-42c7-aaab-0f68a0c9d920', '黄水晶', 'CITRINE', '黄水晶珠宝系列，以其明亮的黄色调和繁荣能量著称，象征成功与财富，为佩戴者带来积极心态与丰盛吸引。', 'f719f82c-39b4-4a61-8884-058aebea1c7f', 'LEVEL_3', NULL, NULL, 't', 'f', 370, '黄水晶珠宝 - 明亮黄色的财富能量饰品', '浏览黄水晶珠宝系列，以其明亮的黄色调和繁荣能量著称。我们提供黄水晶手链、项链、戒指等多种款式，每件作品都精选优质黄水晶，精心制作而成。黄水晶象征成功与财富，能为佩戴者带来积极心态与丰盛吸引，是追求事业成就与物质丰裕的理想配饰。', '黄水晶, 黄水晶珠宝, 财富宝石, 成功饰品', '2025-05-28 03:00:22.45019', '2025-05-28 03:00:22.45019');
INSERT INTO "public"."product_categories" VALUES ('f10b711e-742f-404d-813f-0c2ca8542ff2', '拉长石', 'LABRADORITE', '拉长石珠宝系列，以其神秘的变彩效应和直觉能量著称，象征神秘与内在探索，为佩戴者带来灵感与保护。', 'f719f82c-39b4-4a61-8884-058aebea1c7f', 'LEVEL_3', NULL, NULL, 't', 'f', 380, '拉长石珠宝 - 神秘变彩的直觉能量饰品', '探索拉长石珠宝系列，以其神秘的变彩效应和直觉能量著称。我们提供拉长石手链、项链、戒指等多种款式，每件作品都精选优质拉长石，精心制作而成。拉长石象征神秘与内在探索，能为佩戴者带来灵感与保护，是追求灵性成长与直觉启迪的理想配饰。', '拉长石, 拉长石珠宝, 直觉宝石, 神秘饰品', '2025-05-28 03:00:22.45019', '2025-05-28 03:00:22.45019');
INSERT INTO "public"."product_categories" VALUES ('caf67522-2aed-4394-ad89-1d7ffc447518', '黑曜石', 'BLACK_OBSIDIAN', '黑曜石珠宝系列，以其深邃的黑色和保护能量著称，象征力量与接地，为佩戴者带来安全感与情绪稳定。', 'f719f82c-39b4-4a61-8884-058aebea1c7f', 'LEVEL_3', NULL, NULL, 't', 'f', 390, '黑曜石珠宝 - 深邃黑色的保护力量饰品', '浏览黑曜石珠宝系列，以其深邃的黑色和保护能量著称。我们提供黑曜石手链、项链、戒指等多种款式，每件作品都精选优质黑曜石，精心制作而成。黑曜石象征力量与接地，能为佩戴者带来安全感与情绪稳定，是面对挑战与寻求内心平静的理想配饰。', '黑曜石, 黑曜石珠宝, 保护宝石, 力量饰品', '2025-05-28 03:00:22.45119', '2025-05-28 03:00:22.45119');
INSERT INTO "public"."product_categories" VALUES ('59ccefa3-b1f3-4b0b-9587-e428ba6a205d', '石榴石', 'GARNET', '石榴石珠宝系列，以其浓郁的红色调和活力能量著称，象征热情与生命力，为佩戴者带来激情与再生力量。', 'f719f82c-39b4-4a61-8884-058aebea1c7f', 'LEVEL_3', NULL, NULL, 't', 'f', 400, '石榴石珠宝 - 浓郁红色的热情活力饰品', '探索石榴石珠宝系列，以其浓郁的红色调和活力能量著称。我们提供石榴石手链、项链、戒指等多种款式，每件作品都精选优质石榴石，精心制作而成。石榴石象征热情与生命力，能为佩戴者带来激情与再生力量，是追求活力与情感表达的理想配饰。', '石榴石, 石榴石珠宝, 活力宝石, 红色饰品', '2025-05-28 03:00:22.45219', '2025-05-28 03:00:22.45219');
INSERT INTO "public"."product_categories" VALUES ('05ab7b51-b250-4bbd-9cd2-bb39baf5842e', '珍珠', 'PEARL', '珍珠珠宝系列，以其优雅的光泽和经典美感著称，象征纯洁与高贵，展现女性的温婉与魅力，是永不过时的珍贵饰品。', 'f719f82c-39b4-4a61-8884-058aebea1c7f', 'LEVEL_3', NULL, NULL, 't', 'f', 410, '珍珠珠宝 - 典雅光泽的高贵饰品', '浏览珍珠珠宝系列，以其优雅的光泽和经典美感著称。我们提供珍珠手链、项链、戒指、耳环等多种款式，每件作品都精选优质珍珠，精心制作而成。珍珠象征纯洁与高贵，展现女性的温婉与魅力，是永不过时的珍贵饰品，适合各种场合佩戴，彰显优雅气质。', '珍珠, 珍珠珠宝, 高贵饰品, 典雅配饰', '2025-05-28 03:00:22.453192', '2025-05-28 03:00:22.453192');
INSERT INTO "public"."product_categories" VALUES ('8e75b808-6952-465c-88a9-a5babf0f14c3', '虎眼石', 'TIGER_EYE', '虎眼石珠宝系列，以其独特的金黄色调和猫眼效应著称，象征信心与勇气，为佩戴者带来力量与清晰视野。', 'f719f82c-39b4-4a61-8884-058aebea1c7f', 'LEVEL_3', NULL, NULL, 't', 'f', 420, '虎眼石珠宝 - 金黄色调的力量视野饰品', '探索虎眼石珠宝系列，以其独特的金黄色调和猫眼效应著称。我们提供虎眼石手链、项链、戒指等多种款式，每件作品都精选优质虎眼石，精心制作而成。虎眼石象征信心与勇气，能为佩戴者带来力量与清晰视野，是追求自我肯定与突破困境的理想配饰。', '虎眼石, 虎眼石珠宝, 力量宝石, 金黄色饰品', '2025-05-28 03:00:22.454189', '2025-05-28 03:00:22.454189');
INSERT INTO "public"."product_categories" VALUES ('38d52275-417b-4327-86dc-22fad45e0301', '萤石', 'FLUORITE', '萤石珠宝系列，以其多样的色彩和心灵能量著称，象征平衡与和谐，为佩戴者带来情绪稳定与精神集中。', 'f719f82c-39b4-4a61-8884-058aebea1c7f', 'LEVEL_3', NULL, NULL, 't', 'f', 430, '萤石珠宝 - 多彩心灵的平衡和谐饰品', '浏览萤石珠宝系列，以其多样的色彩和心灵能量著称。我们提供萤石手链、项链、戒指等多种款式，每件作品都精选优质萤石，精心制作而成。萤石象征平衡与和谐，能为佩戴者带来情绪稳定与精神集中，是追求心灵平静与精神成长的理想配饰。', '萤石, 萤石珠宝, 心灵宝石, 多彩饰品', '2025-05-28 03:00:22.454189', '2025-05-28 03:00:22.454189');
INSERT INTO "public"."product_categories" VALUES ('7b1b08fb-b5ba-4280-9e80-afb2ce9e439a', '玛瑙', 'AGATE', '玛瑙珠宝系列，以其独特的纹路和保护能量著称，象征稳定与勇气，为佩戴者带来平衡与耐心。', 'f719f82c-39b4-4a61-8884-058aebea1c7f', 'LEVEL_3', NULL, NULL, 't', 'f', 440, '玛瑙珠宝 - 独特纹路的稳定保护饰品', '探索玛瑙珠宝系列，以其独特的纹路和保护能量著称。我们提供玛瑙手链、项链、戒指等多种款式，每件作品都精选优质玛瑙，精心制作而成。玛瑙象征稳定与勇气，能为佩戴者带来平衡与耐心，是面对生活挑战与寻求内心平静的理想配饰。', '玛瑙, 玛瑙珠宝, 稳定宝石, 纹路饰品', '2025-05-28 03:00:22.455189', '2025-05-28 03:00:22.455189');
INSERT INTO "public"."product_categories" VALUES ('af046d5b-65f2-4cef-99c3-b0723c142b50', '朱砂', 'CINNABAR', '朱砂珠宝系列，以其鲜艳的红色和守护能量著称，象征平安与吉祥，为佩戴者带来保护与积极气场。', 'f719f82c-39b4-4a61-8884-058aebea1c7f', 'LEVEL_3', NULL, NULL, 't', 'f', 450, '朱砂珠宝 - 鲜红守护的平安吉祥饰品', '浏览朱砂珠宝系列，以其鲜艳的红色和守护能量著称。我们提供朱砂手链、项链、戒指等多种款式，每件作品都精选优质朱砂，精心制作而成。朱砂象征平安与吉祥，能为佩戴者带来保护与积极气场，是祈求好运与驱邪避灾的理想配饰。', '朱砂, 朱砂珠宝, 平安饰品, 红色宝石', '2025-05-28 03:00:22.45619', '2025-05-28 03:00:22.45619');
INSERT INTO "public"."product_categories" VALUES ('2dba15fb-c40b-471b-8192-40552834bc90', '绿东陵', 'GREEN_AVENTURINE', '绿东陵珠宝系列，以其清新的绿色和丰盛能量著称，象征成长与机遇，为佩戴者带来积极变化与幸运吸引。', 'f719f82c-39b4-4a61-8884-058aebea1c7f', 'LEVEL_3', NULL, NULL, 't', 'f', 460, '绿东陵珠宝 - 清新绿色的丰盛机遇饰品', '探索绿东陵珠宝系列，以其清新的绿色和丰盛能量著称。我们提供绿东陵手链、项链、戒指等多种款式，每件作品都精选优质绿东陵，精心制作而成。绿东陵象征成长与机遇，能为佩戴者带来积极变化与幸运吸引，是追求事业发展与生活改善的理想配饰。', '绿东陵, 绿东陵珠宝, 丰盛宝石, 绿色饰品', '2025-05-28 03:00:22.457189', '2025-05-28 03:00:22.457189');
INSERT INTO "public"."product_categories" VALUES ('226f6a96-b492-442f-9a26-f3b6698a5653', '青金石', 'LAPIS_LAZULI', '青金石珠宝系列，以其深邃的蓝色和皇家气质著称，象征智慧与真相，为佩戴者带来洞察力与精神启迪。', 'f719f82c-39b4-4a61-8884-058aebea1c7f', 'LEVEL_3', NULL, NULL, 't', 'f', 470, '青金石珠宝 - 皇家蓝色的智慧真相饰品', '浏览青金石珠宝系列，以其深邃的蓝色和皇家气质著称。我们提供青金石手链、项链、戒指等多种款式，每件作品都精选优质青金石，精心制作而成。青金石象征智慧与真相，能为佩戴者带来洞察力与精神启迪，是追求知识与心灵成长的理想配饰。', '青金石, 青金石珠宝, 智慧宝石, 皇家饰品', '2025-05-28 03:00:22.457189', '2025-05-28 03:00:22.457189');
INSERT INTO "public"."product_categories" VALUES ('ef4056e2-0c63-4f44-8f64-bf4a9b66d56d', '白水晶', 'CLEAR_QUARTZ', '白水晶珠宝系列，以其纯净的透明度和放大能量著称，象征纯洁与清晰，为佩戴者带来心灵净化与能量提升。', 'f719f82c-39b4-4a61-8884-058aebea1c7f', 'LEVEL_3', NULL, NULL, 't', 'f', 480, '白水晶珠宝 - 纯净透明的能量提升饰品', '探索白水晶珠宝系列，以其纯净的透明度和放大能量著称。我们提供白水晶手链、项链、戒指等多种款式，每件作品都精选优质白水晶，精心制作而成。白水晶象征纯洁与清晰，能为佩戴者带来心灵净化与能量提升，是追求灵性成长与身心平衡的理想配饰。', '白水晶, 白水晶珠宝, 能量宝石, 纯净饰品', '2025-05-28 03:00:22.458189', '2025-05-28 03:00:22.458189');
INSERT INTO "public"."product_categories" VALUES ('cb55c3b8-a243-4e26-8e7c-9f446faf9fe8', '按符号', 'BY_SYMBOL', '根据文化符号分类的珠宝首饰系列，从莲花到大卫之星，每种符号都蕴含深厚的文化意义与精神价值，为您的饰品增添特别内涵。', '0b250eab-a67a-4d50-bdfc-2750efcd6142', 'LEVEL_2', NULL, NULL, 't', 'f', 40, '符号珠宝首饰 - 探索文化象征的魅力', '浏览根据文化符号分类的珠宝首饰系列，从莲花到大卫之星，每种符号都蕴含深厚的文化意义与精神价值。我们精选多种文化元素，精心制作成手链、项链、戒指等饰品，不仅展现独特设计，更传递符号背后的寓意，是表达信念与追求的理想选择。', '符号珠宝, 文化饰品, 莲花珠宝, 大卫之星, 佛像饰品', '2025-05-28 03:00:22.459423', '2025-05-28 03:00:22.459423');
INSERT INTO "public"."product_categories" VALUES ('d8d198c2-c5fd-484e-a4d2-d0e83c5c034d', '莲花', 'LOTUS', '莲花符号珠宝系列，象征纯洁与重生，展现优雅绽放的姿态，为佩戴者带来精神启迪与心灵净化。', 'cb55c3b8-a243-4e26-8e7c-9f446faf9fe8', 'LEVEL_3', NULL, NULL, 't', 'f', 500, '莲花珠宝 - 纯洁重生的优雅精神饰品', '探索莲花符号珠宝系列，象征纯洁与重生。我们提供莲花造型的手链、项链、戒指等多种款式，每件作品都精心设计，展现莲花优雅绽放的姿态。莲花珠宝为佩戴者带来精神启迪与心灵净化，是追求内心平静与精神成长的理想配饰，展现东方文化的深厚底蕴。', '莲花珠宝, 莲花饰品, 纯洁象征, 精神珠宝', '2025-05-28 03:00:22.459423', '2025-05-28 03:00:22.459423');
INSERT INTO "public"."product_categories" VALUES ('196c8399-4eb7-47dc-9db1-2cf06527f24c', '佛陀', 'BUDDHA', '佛陀符号珠宝系列，以庄严的佛像传递智慧与慈悲，为佩戴者带来内心的安宁与祝福，展现佛教文化的深邃内涵。', 'cb55c3b8-a243-4e26-8e7c-9f446faf9fe8', 'LEVEL_3', NULL, NULL, 't', 'f', 510, '佛陀珠宝 - 智慧慈悲的佛教精神饰品', '浏览佛陀符号珠宝系列，以庄严的佛像传递智慧与慈悲。我们提供多种佛像造型的手链、项链、吊坠等饰品，每件作品都精心制作，展现佛教文化的深邃内涵。佛陀珠宝为佩戴者带来内心的安宁与祝福，是追求精神寄托与心灵平静的理想配饰，适合冥想与日常佩戴。', '佛陀珠宝, 佛像饰品, 智慧象征, 佛教饰品', '2025-05-28 03:00:22.460411', '2025-05-28 03:00:22.460411');
INSERT INTO "public"."product_categories" VALUES ('5597ec2d-7c51-4ed7-ad2b-484275f0a0c0', '禅与阴阳', 'ZEN_YIN_YANG', '禅与阴阳符号珠宝系列，融合东方哲学思想，展现平衡与和谐之美，为佩戴者带来心灵平静与内在稳定。', 'cb55c3b8-a243-4e26-8e7c-9f446faf9fe8', 'LEVEL_3', NULL, NULL, 't', 'f', 520, '禅与阴阳珠宝 - 东方哲学的平衡和谐饰品', '探索禅与阴阳符号珠宝系列，融合东方哲学思想。我们提供禅意图案、阴阳符号等设计的手链、项链、戒指等饰品，每件作品都精心打造，展现平衡与和谐之美。禅与阴阳珠宝为佩戴者带来心灵平静与内在稳定，是追求身心平衡与哲学思考的理想配饰，展现东方智慧的独特魅力。', '禅珠宝, 阴阳饰品, 哲学珠宝, 东方文化', '2025-05-28 03:00:22.460411', '2025-05-28 03:00:22.460411');
INSERT INTO "public"."product_categories" VALUES ('0c448a28-1e50-4854-866b-f046e22d0d58', '象神与大象', 'GANESH_ELEPHANT', '象神与大象符号珠宝系列，象征智慧与成功，去除障碍，为佩戴者带来好运与繁荣，展现印度文化的神秘魅力。', 'cb55c3b8-a243-4e26-8e7c-9f446faf9fe8', 'LEVEL_3', NULL, NULL, 't', 'f', 530, '象神与大象珠宝 - 智慧成功的印度文化饰品', '浏览象神与大象符号珠宝系列，象征智慧与成功，去除障碍。我们提供象神 Ganesh 造型、大象图案等设计的手链、项链、吊坠等饰品，每件作品都精心制作，展现印度文化的神秘魅力。象神与大象珠宝为佩戴者带来好运与繁荣，是祈求智慧与突破障碍的理想配饰，适合追求成功与积极变化的人士。', '象神珠宝, 大象饰品, 印度文化, 智慧象征', '2025-05-28 03:00:22.461426', '2025-05-28 03:00:22.461426');
INSERT INTO "public"."product_categories" VALUES ('c532521d-7228-43ba-a95a-57c0cc2fd1d5', '六字真言', 'OM_MANI_PADME_HUM', '六字真言符号珠宝系列，承载佛教祈愿与祝福，展现精神力量，为佩戴者带来心灵保护与内在平静。', 'cb55c3b8-a243-4e26-8e7c-9f446faf9fe8', 'LEVEL_3', NULL, NULL, 't', 'f', 540, '六字真言珠宝 - 佛教祈愿的精神力量饰品', '探索六字真言符号珠宝系列，承载佛教祈愿与祝福。我们提供刻有 ''Om Mani Padme Hum'' 的手链、项链、吊坠等饰品，每件作品都精心制作，展现佛教文化的精神力量。六字真言珠宝为佩戴者带来心灵保护与内在平静，是冥想辅助与精神寄托的理想配饰，适合追求心灵成长与佛教修行的人士。', '六字真言珠宝, 佛教饰品, 精神力量, 佛教祈愿', '2025-05-28 03:00:22.46241', '2025-05-28 03:00:22.46241');
INSERT INTO "public"."product_categories" VALUES ('4c88f233-12d9-4718-b52e-9bedbe5685fb', '锦鲤', 'KOI_FISH', '锦鲤符号珠宝系列，象征好运与坚持，展现逆流而上的精神，为佩戴者带来积极能量与成功吸引。', 'cb55c3b8-a243-4e26-8e7c-9f446faf9fe8', 'LEVEL_3', NULL, NULL, 't', 'f', 550, '锦鲤珠宝 - 好运坚持的积极能量饰品', '浏览锦鲤符号珠宝系列，象征好运与坚持。我们提供锦鲤造型的手链、项链、吊坠等饰品，每件作品都精心设计，展现锦鲤逆流而上的精神。锦鲤珠宝为佩戴者带来积极能量与成功吸引，是追求目标与克服困难的理想配饰，展现东方文化的吉祥寓意。', '锦鲤珠宝, 锦鲤饰品, 好运象征, 成功能量', '2025-05-28 03:00:22.46241', '2025-05-28 03:00:22.46241');
INSERT INTO "public"."product_categories" VALUES ('2b39d691-793e-47d9-ae37-adb468fd7d1c', '貔貅', 'PIXIU', '貔貅符号珠宝系列，象征招财进宝与辟邪，为佩戴者带来财富吸引与保护，展现中国传统文化的吉祥寓意。', 'cb55c3b8-a243-4e26-8e7c-9f446faf9fe8', 'LEVEL_3', NULL, NULL, 't', 'f', 560, '貔貅珠宝 - 招财进宝的辟邪吉祥饰品', '探索貔貅符号珠宝系列，象征招财进宝与辟邪。我们提供貔貅造型的手链、项链、吊坠等饰品，每件作品都精心制作，展现中国传统文化的吉祥寓意。貔貅珠宝为佩戴者带来财富吸引与保护，是祈求财运亨通与平安顺利的理想配饰，适合商业人士与追求吉祥的人士。', '貔貅珠宝, 貔貅饰品, 招财吉祥, 中国传统文化', '2025-05-28 03:00:22.46341', '2025-05-28 03:00:22.46341');
INSERT INTO "public"."product_categories" VALUES ('d7f3591b-59d4-41d3-a9d8-b21120718307', '中国生肖', 'THE_CHINESE_ZODIAC', '中国生肖符号珠宝系列，以十二生肖为主题，展现个性与命运连接，为佩戴者带来属相守护与文化认同，是传统节日与日常佩戴的理想选择。', 'cb55c3b8-a243-4e26-8e7c-9f446faf9fe8', 'LEVEL_3', NULL, NULL, 't', 'f', 570, '中国生肖珠宝 - 十二生肖的文化守护饰品', '浏览中国生肖符号珠宝系列，以十二生肖为主题。我们提供鼠、牛、虎等生肖造型的手链、项链、吊坠等饰品，每件作品都精心设计，展现个性与命运连接。生肖珠宝为佩戴者带来属相守护与文化认同，是传统节日赠送与日常佩戴的理想选择，展现中国传统文化的独特魅力与属相寓意。', '生肖珠宝, 生肖饰品, 中国传统文化, 十二生肖', '2025-05-28 03:00:22.464422', '2025-05-28 03:00:22.464422');
INSERT INTO "public"."product_categories" VALUES ('95875f70-2d10-47f4-8aa5-b43e8ee7eeae', '生命之树', 'THE_TREE_OF_LIFE', '生命之树符号珠宝系列，象征成长与连接，展现自然和谐之美，为佩戴者带来生命力与平衡感，是追求精神成长的理想配饰。', 'cb55c3b8-a243-4e26-8e7c-9f446faf9fe8', 'LEVEL_3', NULL, NULL, 't', 'f', 580, '生命之树珠宝 - 成长连接的自然和谐饰品', '探索生命之树符号珠宝系列，象征成长与连接。我们提供生命之树图案的手链、项链、吊坠等饰品，每件作品都精心制作，展现自然和谐之美。生命之树珠宝为佩戴者带来生命力与平衡感，是追求精神成长与自然连接的理想配饰，展现跨文化的共同价值与生命意义。', '生命之树珠宝, 自然饰品, 成长象征, 和谐寓意', '2025-05-28 03:00:22.464422', '2025-05-28 03:00:22.464422');
INSERT INTO "public"."product_categories" VALUES ('6c14399d-4d4d-4eb9-8f9e-0ed36241dce8', '法蒂玛之手', 'HAMSA', '法蒂玛之手符号珠宝系列，象征保护与好运，以开放手掌设计驱散负面能量，为佩戴者带来平安与祝福，展现中东文化的深厚底蕴。', 'cb55c3b8-a243-4e26-8e7c-9f446faf9fe8', 'LEVEL_3', NULL, NULL, 't', 'f', 590, '法蒂玛之手珠宝 - 保护好运的中东文化饰品', '浏览法蒂玛之手符号珠宝系列，象征保护与好运。我们提供法蒂玛之手造型的手链、项链、吊坠等饰品，每件作品都精心设计，展现中东文化的深厚底蕴。法蒂玛之手珠宝以开放手掌设计驱散负面能量，为佩戴者带来平安与祝福，是祈求保护与吸引好运的理想配饰，适合不同文化背景的人士佩戴。', '法蒂玛之手珠宝, 保护饰品, 中东文化, 好运象征', '2025-05-28 03:00:22.46541', '2025-05-28 03:00:22.46541');
INSERT INTO "public"."product_categories" VALUES ('f6867f3e-5cba-4721-a8d0-17d1a82332ca', '邪眼', 'EVIL_EYE', '邪眼符号珠宝系列，象征保护与净化，以蓝色眼睛设计抵御邪恶目光，为佩戴者带来平安与正能量，展现地中海文化的独特魅力。', 'cb55c3b8-a243-4e26-8e7c-9f446faf9fe8', 'LEVEL_3', NULL, NULL, 't', 'f', 600, '邪眼珠宝 - 保护净化的地中海文化饰品', '探索邪眼符号珠宝系列，象征保护与净化。我们提供蓝色眼睛造型的手链、项链、吊坠等饰品，每件作品都精心制作，展现地中海文化的独特魅力。邪眼珠宝以经典设计抵御邪恶目光，为佩戴者带来平安与正能量，是祈求保护与驱邪避灾的理想配饰，流行于多种文化中，寓意深远。', '邪眼珠宝, 保护饰品, 蓝色眼睛, 地中海文化', '2025-05-28 03:00:22.46541', '2025-05-28 03:00:22.46541');
INSERT INTO "public"."product_categories" VALUES ('eeee67a5-15b8-4c5e-914f-a4b7b7a8160e', '大卫之星', 'STAR_OF_DAVID', '大卫之星符号珠宝系列，象征犹太文化与精神信仰，以六角星设计展现智慧与神圣几何，为佩戴者带来文化认同与精神力量。', 'cb55c3b8-a243-4e26-8e7c-9f446faf9fe8', 'LEVEL_3', NULL, NULL, 't', 'f', 610, '大卫之星珠宝 - 犹太文化的智慧信仰饰品', '浏览大卫之星符号珠宝系列，象征犹太文化与精神信仰。我们提供六角星造型的手链、项链、吊坠等饰品，每件作品都精心设计，展现智慧与神圣几何的完美结合。大卫之星珠宝为佩戴者带来文化认同与精神力量，是犹太文化传承与信仰表达的理想配饰，展现深厚的历史底蕴与宗教意义。', '大卫之星珠宝, 犹太文化, 六角星饰品, 信仰象征', '2025-05-28 03:00:22.466411', '2025-05-28 03:00:22.466411');
INSERT INTO "public"."product_categories" VALUES ('bf42e9fa-ccaa-4255-9c14-ca52919dfe13', '菩提子念珠', 'BODHI_SEED_MALAS', '菩提子念珠系列，采用天然菩提子精心制作，展现质朴与灵性之美，是传统冥想与祈福的理想工具，承载深厚的文化意义。', '32b50225-0657-4de3-ae51-959f1de68282', 'LEVEL_2', NULL, NULL, 't', 'f', 10, 'Bodhi Seed Malas - 菩提子念珠系列', '探索菩提子念珠系列，采用天然菩提子精心制作。这些念珠展现质朴与灵性之美，是传统冥想与祈福的理想工具。菩提子象征觉悟与精神成长，每颗珠子都经过精细打磨，为您带来独特质感与深厚的文化体验，是冥想修行与日常佩戴的完美结合。', '菩提子念珠, Bodhi Seed Malas, 冥想念珠, 传统祈福', '2025-05-28 03:00:22.467915', '2025-05-28 03:00:22.467915');
INSERT INTO "public"."product_categories" VALUES ('7f438404-11b4-493d-b26d-fc68b64c4beb', '木质念珠', 'WOOD_MALAS', '木质念珠系列，选用优质木材制作，散发自然木质香气，展现温暖质感与大地能量，为冥想带来平静与接地感。', '32b50225-0657-4de3-ae51-959f1de68282', 'LEVEL_2', NULL, NULL, 't', 'f', 20, 'Wood Malas - 木质念珠系列', '浏览木质念珠系列，选用优质木材精心制作。这些念珠散发自然木质香气，展现温暖质感与大地能量。木质念珠为冥想带来平静与接地感，帮助您连接自然与内在力量。每串念珠都经过精细打磨，确保舒适握感，是追求自然生活方式与精神平衡的理想配饰。', '木质念珠, Wood Malas, 自然冥想, 木质香气', '2025-05-28 03:00:22.468922', '2025-05-28 03:00:22.468922');
INSERT INTO "public"."product_categories" VALUES ('45969b85-fb2b-479a-93d5-2e97f3e28db5', '宝石念珠', 'GEMSTONE_MALAS', '宝石念珠系列，镶嵌多种珍贵宝石，融合美丽与能量疗愈特性，为佩戴者带来独特风格与精神平衡，展现个性与灵性魅力。', '32b50225-0657-4de3-ae51-959f1de68282', 'LEVEL_2', NULL, NULL, 't', 'f', 30, '宝石念珠系列', '探索宝石念珠系列，镶嵌多种珍贵宝石，如紫水晶、绿松石、石榴石等。这些念珠融合美丽与能量疗愈特性，为佩戴者带来独特风格与精神平衡。每颗宝石都经过精心挑选与打磨，展现独特光泽与能量频率，帮助增强冥想效果、提升情绪状态。宝石念珠不仅是冥想工具，更是展现个性与灵性魅力的时尚配饰，适合各种场合佩戴。', '宝石念珠, Gemstone Malas, 能量疗愈, 宝石饰品', '2025-05-28 03:00:22.46992', '2025-05-28 03:00:22.46992');
INSERT INTO "public"."product_categories" VALUES ('ae9c84d4-2d44-4987-9695-69f81dba90de', '手腕念珠', 'WRIST_MALAS', '手腕念珠系列，专为手腕佩戴设计，小巧精致且方便日常使用，将冥想修行融入日常生活，成为表达信仰与风格的便捷配饰。', '32b50225-0657-4de3-ae51-959f1de68282', 'LEVEL_2', NULL, NULL, 't', 'f', 40, '手腕念珠系列', '浏览手腕念珠系列，专为手腕佩戴设计。这些念珠小巧精致，方便日常使用，将冥想修行融入日常生活。手腕念珠采用多种材质，包括菩提子、宝石、木材等，展现不同风格与能量。佩戴手腕念珠不仅是一种时尚选择，更是随时提醒自己保持觉知、平衡情绪的精神象征，适合在工作、学习、旅行等各种场合佩戴，为您的生活增添一份宁静与力量。', '手腕念珠, Wrist Malas, 日常冥想, 便捷配饰', '2025-05-28 03:00:22.47092', '2025-05-28 03:00:22.47092');
INSERT INTO "public"."product_categories" VALUES ('f38e7690-4f9c-4aea-b82d-55697e4c342b', '稀有沉香念珠', 'RARE_AGARWOOD_MALAS', '稀有沉香念珠系列，采用珍贵沉香木制作，散发独特木质香气，具有高度灵性价值，为高级冥想与收藏的理想选择，展现奢华与神圣氛围。', '32b50225-0657-4de3-ae51-959f1de68282', 'LEVEL_2', NULL, NULL, 't', 'f', 50, '稀有沉香念珠系列', '探索稀有沉香念珠系列，采用珍贵沉香木精心制作。这些念珠散发独特木质香气，具有高度灵性价值，能提升冥想深度与精神连接。沉香木在东方文化中被视为神圣材料，象征高贵与精神升华。每串沉香念珠都经过精细工艺处理，确保香气持久与质感优良。作为高级冥想工具与收藏品，沉香念珠展现奢华与神圣氛围，是追求精神境界与品味生活的理想选择，适合特别场合与日常珍藏。', '沉香念珠, Agarwood Malas, 珍贵木材, 灵性冥想', '2025-05-28 03:00:22.47192', '2025-05-28 03:00:22.47192');
INSERT INTO "public"."product_categories" VALUES ('a946fd9d-44a9-4ca8-b197-86d0fb3f99c3', '冥想练习', 'MEDITATION_PRACTICE', '冥想练习必备工具，包括唱钵、西藏铃铛等多种辅助用品，帮助您集中注意力，进入深度冥想状态，提升修行效果。', '7f0a0b8e-70ed-4600-bac5-7ad280ac6191', 'LEVEL_2', NULL, NULL, 't', 'f', 10, '冥想练习工具 - 提升修行效果', '探索冥想练习必备工具系列，包括唱钵、西藏铃铛、拇指琴等多种辅助用品。这些工具通过声音振动帮助您集中注意力，进入深度冥想状态。我们的产品经过精心挑选与测试，确保音质纯净，效果显著，适合各种冥想传统与个人修行方式，是提升冥想体验与效果的理想选择。', '冥想练习, 冥想工具, 唱钵, 西藏铃铛', '2025-05-28 03:00:22.472922', '2025-05-28 03:00:22.472922');
INSERT INTO "public"."product_categories" VALUES ('0611edfb-ec07-46ed-ae49-7b17caba9826', '唱钵', 'SINGING_BOWLS', '精选各种尺寸与材质的唱钵，通过振动产生和谐声音，帮助平衡能量，进入深度放松状态，是冥想与声音疗愈的理想工具。', 'a946fd9d-44a9-4ca8-b197-86d0fb3f99c3', 'LEVEL_3', NULL, NULL, 't', 'f', 100, '唱钵 - 声音疗愈与冥想工具', '探索精选唱钵系列，各种尺寸与材质可选。唱钵通过振动产生和谐声音，帮助平衡能量，进入深度放松状态。我们的唱钵经过严格挑选，确保音质纯净，效果显著，适用于冥想、声音疗愈、瑜伽等多种场合，是提升修行体验与身心平衡的理想选择。', '唱钵, 声音疗愈, 冥想工具, 能量平衡', '2025-05-28 03:00:22.473921', '2025-05-28 03:00:22.473921');
INSERT INTO "public"."product_categories" VALUES ('ff51bf02-6f4b-4337-ba76-b5c034ad616e', '西藏铜铃', 'TIBETAN_TINGSHA_BELLS', '传统西藏铜铃，以清脆声音标志冥想阶段，帮助集中注意力，创造神圣氛围，是藏传佛教修行与个人冥想的珍贵辅助工具。', 'a946fd9d-44a9-4ca8-b197-86d0fb3f99c3', 'LEVEL_3', NULL, NULL, 't', 'f', 110, '西藏铜铃 - 标志冥想阶段的神圣工具', '浏览传统西藏铜铃系列，以清脆声音标志冥想阶段。我们的西藏铜铃采用传统工艺制作，声音纯净悠扬，帮助集中注意力，创造神圣氛围。这些铜铃在藏传佛教修行中具有重要地位，同样适合个人冥想使用，为您的修行带来传统智慧与精神力量，是连接古老文化与现代修行的桥梁。', '西藏铜铃, 冥想标志, 神圣氛围, 佛教修行', '2025-05-28 03:00:22.474922', '2025-05-28 03:00:22.474922');
INSERT INTO "public"."product_categories" VALUES ('6c858d52-05f1-4629-bcc9-461594625ea0', '拇指琴', 'KALIMBA_THUMB_PIANO', '便携式拇指琴，以柔和旋律辅助冥想与放松，激发创意，带来愉悦心灵体验，是旅行与日常修行的理想伴侣。', 'a946fd9d-44a9-4ca8-b197-86d0fb3f99c3', 'LEVEL_3', NULL, NULL, 't', 'f', 120, '拇指琴 - 柔和旋律的冥想辅助工具', '探索便携式拇指琴系列，以柔和旋律辅助冥想与放松。我们的拇指琴采用优质材料制作，音色温暖悦耳，激发创意灵感。这种小巧乐器适合旅行与日常修行使用，随时随地为您的心灵带来愉悦体验。无论是冥想前的准备、修行中的辅助，还是放松时刻的陪伴，拇指琴都能帮助您进入平和心境，提升整体修行质量。', '拇指琴, 冥想音乐, 便携乐器, 心灵放松', '2025-05-28 03:00:22.474922', '2025-05-28 03:00:22.474922');
INSERT INTO "public"."product_categories" VALUES ('3ffb427b-f473-40bf-9ece-3f4e927bb217', '冥想禅园', 'MEDITATION_ZEN_GARDENS', '微型禅意花园套装，通过布置砂石与小景观创造冥想焦点，培养专注力与耐心，展现日本禅宗美学，为室内空间增添宁静氛围。', 'a946fd9d-44a9-4ca8-b197-86d0fb3f99c3', 'LEVEL_3', NULL, NULL, 't', 'f', 130, '冥想禅园 - 日本禅宗美学的室内冥想工具', '浏览微型禅意花园套装系列，通过布置砂石与小景观创造冥想焦点。我们的禅园套装精心设计，展现日本禅宗美学精髓。这些套装帮助培养专注力与耐心，为室内空间增添宁静氛围。无论是放置在书桌、床头柜还是窗台，禅意花园都能成为您日常冥想的视觉焦点，引导心灵进入平静状态，是连接自然与精神世界的理想桥梁，特别适合城市生活中的心灵避难所创建。', '禅意花园, 禅宗美学, 冥想焦点, 日本文化', '2025-05-28 03:00:22.475923', '2025-05-28 03:00:22.475923');
INSERT INTO "public"."product_categories" VALUES ('0243e37b-9373-40e0-b9ac-82f5bd79d01e', '冥想坐垫', 'MEDITATION_CUSHIONS', '精心设计的冥想坐垫，提供舒适支撑，促进正确坐姿，延长冥想时间，采用天然材料制作，展现简约风格，是打造理想冥想空间的基础用品。', 'a946fd9d-44a9-4ca8-b197-86d0fb3f99c3', 'LEVEL_3', NULL, NULL, 't', 'f', 140, '冥想坐垫 - 舒适支撑的修行基础', '探索冥想坐垫系列，精心设计提供舒适支撑。我们的坐垫采用天然材料如有机棉、亚麻、荞麦壳等制作，确保透气性与耐用性。坐垫高度适中，帮助保持脊柱自然曲线，促进正确坐姿，延长冥想时间。简约风格设计融入各种室内装饰，为您的冥想空间增添和谐氛围。无论是传统盘腿坐姿还是椅子辅助冥想，我们都提供适合的坐垫选择，让身体的舒适成为心灵平静的基础。', '冥想坐垫, 舒适支撑, 正确坐姿, 禅修用品', '2025-05-28 03:00:22.47693', '2025-05-28 03:00:22.47693');
INSERT INTO "public"."product_categories" VALUES ('d7e4bb4b-e20d-4312-9350-065ebda9dc6a', '舌鼓', 'TONGUE_DRUM', '疗愈舌鼓，通过低频振动与和谐音阶创造沉浸式声音体验，帮助深度放松，释放压力，是声音疗愈与团体冥想的理想乐器。', 'a946fd9d-44a9-4ca8-b197-86d0fb3f99c3', 'LEVEL_3', NULL, NULL, 't', 'f', 150, '舌鼓 - 低频振动的深度放松乐器', '浏览疗愈舌鼓系列，通过低频振动与和谐音阶创造沉浸式声音体验。我们的舌鼓采用优质钢材制作，音色深沉悠扬，帮助深度放松，释放累积压力。这种现代乐器结合古老声音疗愈原理，适合个人冥想、团体修行以及声音疗愈师使用。舌鼓的简单演奏方式与强大疗愈效果使其成为初学者与专业人士的理想选择，为您的修行带来全新维度的声音能量体验。', '舌鼓, 声音疗愈, 低频振动, 团体冥想', '2025-05-28 03:00:22.477922', '2025-05-28 03:00:22.477922');
INSERT INTO "public"."product_categories" VALUES ('906adfdf-8b62-48bc-8c3d-80e0dd3fc70f', '精神修行', 'SPIRITUAL_PRACTICE', '精神修行辅助用品，包括香薰炉与香料、精油与疗愈工具、水晶宝石等，帮助净化空间、平衡能量，提升修行效果，展现自然能量的疗愈力量。', '7f0a0b8e-70ed-4600-bac5-7ad280ac6191', 'LEVEL_2', NULL, NULL, 't', 'f', 20, '精神修行用品 - 自然能量的疗愈辅助', '探索精神修行辅助用品系列，包括香薰炉与香料、精油与疗愈工具、水晶宝石等。这些产品帮助净化空间、平衡能量，提升修行效果。我们精选全球优质材料，结合传统智慧与现代科学，展现自然能量的疗愈力量。无论是每日修行、特殊仪式还是家居能量维护，都能找到适合的用品，为您的精神旅程增添支持与保护，引导您走向内在平和与整体健康。', '精神修行, 香薰用品, 精油疗愈, 水晶能量', '2025-05-28 03:00:22.478429', '2025-05-28 03:00:22.478429');
INSERT INTO "public"."product_categories" VALUES ('7f0a0b8e-70ed-4600-bac5-7ad280ac6191', '冥想用品', 'MEDITATION', '探索丰富的冥想用品系列，包括冥想练习工具、精神修行辅助品以及创建神圣空间的装饰品，帮助您打造理想的冥想环境，促进内心平静与精神成长。', NULL, 'LEVEL_1', NULL, NULL, 't', 'f', 5, '冥想用品 - 打造理想冥想环境', '探索丰富的冥想用品系列，包括冥想练习工具、精神修行辅助品以及创建神圣空间的装饰品。我们的产品精心挑选，帮助您打造理想的冥想环境，促进内心平静与精神成长。无论是初学者还是资深修行者，都能找到适合自己的冥想辅助工具，提升冥想体验与效果。', '冥想用品, 冥想工具, 精神修行, 神圣空间', '2025-05-28 03:00:22.472922', '2025-05-30 11:12:23.875719');
INSERT INTO "public"."product_categories" VALUES ('96cd6df4-9e77-4b0c-b0db-5d2f8b9c9fea', '香薰炉与香料', 'INCENSE_BURNERS_INCENSE', '多样化的香薰炉与天然香料组合，通过香气净化空间，提升意识状态，创造适合冥想与修行的氛围，传承古老嗅觉疗愈传统。', '906adfdf-8b62-48bc-8c3d-80e0dd3fc70f', 'LEVEL_3', NULL, NULL, 't', 'f', 200, '香薰炉与香料 - 净化空间的嗅觉疗愈工具', '探索香薰炉与香料系列，多样化的组合满足不同修行需求。我们的香薰炉采用陶瓷、金属、石材等材质制作，设计精美实用。搭配的天然香料包括沉香、檀香、藏红花等多种传统配方，通过香气净化空间，提升意识状态。燃烧香料产生的烟雾在许多文化中被视为连接物质与精神世界的桥梁，为您的冥想与修行创造理想氛围，传承古老嗅觉疗愈智慧，是每日修行与特殊仪式的必备用品。', '香薰炉, 天然香料, 净化空间, 嗅觉疗愈', '2025-05-28 03:00:22.478429', '2025-05-28 03:00:22.478429');
INSERT INTO "public"."product_categories" VALUES ('5aa94d1c-036f-44c0-a173-9a8683634f44', '精油与疗愈', 'AROMATHERAPY_HEALING', '精选有机精油与疗愈工具套装，通过芳香疗法缓解身心症状，促进情绪平衡，提升整体健康，结合现代科学与传统智慧的自然疗愈方案。', '906adfdf-8b62-48bc-8c3d-80e0dd3fc70f', 'LEVEL_3', NULL, NULL, 't', 'f', 210, '精油与疗愈 - 芳香疗法的自然健康方案', '浏览精油与疗愈工具套装系列，精选有机精油与专业工具。我们的精油采用纯植物提取，无添加合成成分，确保疗效与安全性。套装包括精油、扩香器、按摩工具等，通过芳香疗法缓解压力、焦虑、失眠等身心症状，促进情绪平衡。每种精油都附有详细使用指南，结合现代科学研究与传统疗愈智慧，为用户提供沉浸式的自然疗愈体验。无论是自我护理还是专业疗愈师使用，都能找到适合的方案，帮助恢复身心和谐，提升整体健康水平。', '有机精油, 芳香疗法, 情绪平衡, 自然疗愈', '2025-05-28 03:00:22.479439', '2025-05-28 03:00:22.479439');
INSERT INTO "public"."product_categories" VALUES ('10a0646e-d445-44c0-bbeb-98b257b9de1e', '水晶', 'CRYSTALS', '各类能量水晶与矿物，根据独特属性辅助不同修行目标，净化负能量，增强直觉，吸引繁荣，是物质与精神连接的桥梁，展现大地能量的多样性。', '906adfdf-8b62-48bc-8c3d-80e0dd3fc70f', 'LEVEL_3', NULL, NULL, 't', 'f', 220, '水晶 - 大地能量的精神疗愈工具', '探索能量水晶与矿物系列，根据独特属性辅助不同修行目标。我们的水晶种类丰富，包括紫水晶、绿松石、黄水晶等，每种水晶都附有详细能量说明。这些天然矿物通过振动频率与能量场影响，帮助净化负能量、增强直觉、吸引繁荣、促进愈合等多种效果。水晶可放置在冥想空间、随身携带或制作成珠宝佩戴，是物质世界与精神维度连接的桥梁。我们提供原矿石、雕刻品、珠宝等多种形式，满足不同需求，展现大地能量的多样性与疗愈力量，为您的修行增添自然支持。', '能量水晶, 矿物疗愈, 净化能量, 直觉增强', '2025-05-28 03:00:22.48043', '2025-05-28 03:00:22.48043');
INSERT INTO "public"."product_categories" VALUES ('0727c619-f8e7-407b-a290-e3cf6a8ef673', '冥想瑜伽气功', 'MEDITATION_YOGA_QIGONG', '结合冥想、瑜伽与气功的辅助用品，包括瑜伽垫、气功课具等，支持身体练习与能量流动，促进身心整合，提升修行深度与效果。', '906adfdf-8b62-48bc-8c3d-80e0dd3fc70f', 'LEVEL_3', NULL, NULL, 't', 'f', 230, '冥想瑜伽气功用品 - 促进身心整合的练习工具', '探索冥想瑜伽气功辅助用品系列，包括专业瑜伽垫、气功课具、冥想坐垫等。我们的产品设计符合人体工学，采用环保材料制作，确保舒适度与耐用性。这些工具支持身体练习与能量流动，帮助正确对齐身体结构，预防练习损伤，提升冥想、瑜伽、气功的修行深度与效果。我们提供不同厚度、材质、尺寸的选择，适合初学者与专业人士使用。通过整合身体、心灵与能量练习，这些用品成为您整体健康维护与精神成长的理想辅助，引导您走向身心和谐与内在力量的觉醒。', '瑜伽气功, 冥想练习, 身心整合, 能量流动', '2025-05-28 03:00:22.481437', '2025-05-28 03:00:22.481437');
INSERT INTO "public"."product_categories" VALUES ('3142edbc-3764-476f-b03b-28511018ddc8', '衣物', 'CLOTHES', '舒适的冥想与瑜伽服装，采用有机棉、亚麻等天然面料制作，设计简约宽松，支持自由活动，为修行创造无拘无束的穿着体验，展现内在平和的外在表达。', '906adfdf-8b62-48bc-8c3d-80e0dd3fc70f', 'LEVEL_3', NULL, NULL, 't', 'f', 240, '冥想瑜伽衣物 - 自然舒适的修行穿着', '浏览冥想与瑜伽服装系列，采用有机棉、亚麻、竹纤维等天然面料制作。我们的设计简约宽松，注重细节，确保穿着舒适度与美观性。衣物款式包括宽松上衣、瑜伽裤、冥想袍等，支持自由活动，适合各种修行姿势。自然色调与精细做工展现内在平和的外在表达，使穿着本身成为修行的一部分。我们注重可持续时尚理念，从材料选择到生产过程都遵循环保标准，为您的修行之旅增添责任感与和谐感，让每一次穿着都成为关爱自己与地球的行动。', '冥想服装, 瑜伽服饰, 天然面料, 舒适穿着', '2025-05-28 03:00:22.481437', '2025-05-28 03:00:22.481437');
INSERT INTO "public"."product_categories" VALUES ('87276629-459e-430f-833f-ed4112f15fa5', '瑜伽辅助工具', 'YOGA_ACCESSORIES', '瑜伽练习辅助工具，包括瑜伽砖、伸展带、倒立辅助器等，帮助正确姿势对齐，深化体式练习，适合不同水平练习者，提升瑜伽修行的安全性与效果。', '906adfdf-8b62-48bc-8c3d-80e0dd3fc70f', 'LEVEL_3', NULL, NULL, 't', 'f', 250, '瑜伽辅助工具 - 提升练习效果的专业用品', '探索瑜伽练习辅助工具系列，包括瑜伽砖、伸展带、倒立辅助器、瑜伽轮等多种产品。这些工具帮助正确姿势对齐，深化体式练习，特别对初学者或有特殊身体状况的练习者提供必要支持。我们的辅助工具采用优质材料制作，设计符合人体工学，确保使用安全与效果显著。通过这些工具的辅助，练习者可以更深入地体验瑜伽体式的益处，预防运动伤害，逐步提升灵活性与力量。我们提供不同材质、尺寸、功能的选择，满足多样化需求，使瑜伽练习更加高效与愉悦，成为您瑜伽旅程中不可或缺的伙伴。', '瑜伽辅助工具, 姿势对齐, 深化体式, 安全练习', '2025-05-28 03:00:22.482429', '2025-05-28 03:00:22.482429');
INSERT INTO "public"."product_categories" VALUES ('7a14b046-e837-4219-b2c8-e3ced0e147d0', '音叉', 'TUNING_FORK', '专业音叉套装，通过精准振动频率促进能量平衡，用于声音疗愈、脉轮调和与冥想引导，是精确能量工作的理想工具，展现声波的疗愈潜力。', '906adfdf-8b62-48bc-8c3d-80e0dd3fc70f', 'LEVEL_3', NULL, NULL, 't', 'f', 260, '音叉 - 精准振动的能量疗愈工具', '浏览专业音叉套装系列，通过精准振动频率促进能量平衡。我们的音叉采用高品质材料制作，频率校准精确，包括脉轮音叉、行星音叉、治疗音叉等多种类型。这些工具用于声音疗愈、脉轮调和、冥想引导以及能量工作，通过声波的物理效应影响身体能量场，帮助恢复平衡与和谐。音叉的使用简单有效，适合疗愈师、冥想指导者以及个人修行者使用。每套音叉都附有详细使用指南与频率说明，帮助您充分发挥其疗愈潜力，探索声波能量的神奇作用，为您的修行带来科学依据的能量支持。', '音叉疗愈, 脉轮调和, 声音疗愈, 能量平衡', '2025-05-28 03:00:22.482429', '2025-05-28 03:00:22.482429');
INSERT INTO "public"."product_categories" VALUES ('b5eca328-9a1a-4164-9441-a8dbcd16cd94', '减压旋钮', 'STRESS_RELIEF_SPINNER', '手持减压旋钮，通过简单旋转动作转移注意力，缓解焦虑与压力，成为日常减压的理想工具，适合各年龄段人群，随时随地恢复平静。', '906adfdf-8b62-48bc-8c3d-80e0dd3fc70f', 'LEVEL_3', NULL, NULL, 't', 'f', 270, '减压旋钮 - 简单有效的日常减压工具', '探索手持减压旋钮系列，通过简单旋转动作转移注意力。我们的减压旋钮设计精美，采用优质材料制作，确保流畅旋转与持久使用。这些工具帮助缓解焦虑、压力、注意力不集中等问题，特别适合办公室工作者、学生、旅行者等需要随时放松的人群。旋钮的使用无需特殊技巧，只需简单旋转即可启动减压效果，成为日常生活中恢复平静的理想工具。我们提供多种款式与颜色选择，满足不同个性需求，让减压也成为一种时尚与享受，帮助您在忙碌生活中找回内心平衡与稳定。', '减压工具, 焦虑缓解, 注意力转移, 日常放松', '2025-05-28 03:00:22.483429', '2025-05-28 03:00:22.483429');
INSERT INTO "public"."product_categories" VALUES ('a8008b40-cb3c-497a-baec-394c4fe102a4', '创建神圣空间', 'CREATE_SACRED_SPACE', '打造神圣空间的装饰与用品，包括祈祷祭坛物品、佛教法器等，帮助建立专属修行环境，增强精神连接，创造有利于冥想与祈祷的氛围，赋予空间特殊意义与能量。', '7f0a0b8e-70ed-4600-bac5-7ad280ac6191', 'LEVEL_2', NULL, NULL, 't', 'f', 30, '神圣空间用品 - 打造专属修行环境', '探索创建神圣空间的装饰与用品系列，包括祈祷祭坛物品、佛教法器等。这些产品帮助建立专属修行环境，增强精神连接，创造有利于冥想与祈祷的氛围。我们的祭坛装饰包括神龛、佛像、蜡烛台、供品盘等多种类型，经过精心设计与制作，展现不同文化与传统的美学价值。佛教法器如金刚杵、佛铃等，承载深厚宗教意义，为修行提供仪式支持。通过布置这些用品，您可以为冥想空间赋予特殊意义与能量，使其成为心灵避难所与精神力量源泉，促进日常修行的深度与效果，连接物质世界与神圣维度。', '神圣空间, 祈祷祭坛, 佛教法器, 精神环境', '2025-05-28 03:00:22.484443', '2025-05-28 03:00:22.484443');
INSERT INTO "public"."product_categories" VALUES ('6e290f22-b73e-481e-bc4d-50b6a212c515', '祈祷祭坛物品', 'PRAYER_ALTAR_ITEMS', '祈祷祭坛装饰与用品，包括神龛、佛像、蜡烛台等，帮助建立个性化修行空间，创造神圣氛围，连接精神传统，增强每日修行的仪式感与专注力。', 'a8008b40-cb3c-497a-baec-394c4fe102a4', 'LEVEL_3', NULL, NULL, 't', 'f', 300, '祈祷祭坛物品 - 个性化神圣空间的装饰', '浏览祈祷祭坛物品系列，包括精美神龛、佛像、蜡烛台、供品盘、经幡等。这些用品帮助建立个性化修行空间，创造神圣氛围，连接不同精神传统。我们的祭坛装饰品来自全球各地，涵盖佛教、印度教、原始萨满等多种文化元素，经过精心挑选与设计，确保品质与美感。通过布置祭坛，您可以为每日修行创造仪式感与专注力，使其成为连接神圣能量的桥梁。每件物品都附有文化背景说明，帮助您深入了解其象征意义，正确使用以增强修行效果，使您的冥想空间成为充满力量与灵感的神圣场所。', '祭坛装饰, 祈祷用品, 神圣氛围, 仪式感', '2025-05-28 03:00:22.484443', '2025-05-28 03:00:22.484443');
INSERT INTO "public"."product_categories" VALUES ('015be9b3-a974-44dd-92c3-341e71b8a0c8', '佛教法器与金刚杵', 'BUDDHIST_BELL_AND_DORJE', '佛教传统法器，包括金刚杵、佛铃等，承载宗教仪式功能，辅助修行者专注咒语、调和能量，是藏传佛教修行与仪式的珍贵工具，展现深厚文化传承。', 'a8008b40-cb3c-497a-baec-394c4fe102a4', 'LEVEL_3', NULL, NULL, 't', 'f', 310, '佛教法器与金刚杵 - 传统修行仪式工具', '探索佛教传统法器系列，包括金刚杵、佛铃、转经筒等珍贵工具。这些法器承载藏传佛教的核心仪式功能，辅助修行者专注咒语、调和能量、开启智慧。我们的法器采用传统工艺制作，选用优质材料如黄铜、红铜、银等，确保音质纯净与使用持久。每件法器都经过僧侣祝福与能量加持，附有详细使用指南与文化背景说明。使用佛教法器不仅能增强修行效果，更是连接古老智慧与传统文化的方式，帮助修行者进入更深层次的精神实践，体验藏传佛教独特的修行方法与精神力量，是佛教修行者的必备圣物，也是对佛教文化感兴趣的探索者的珍贵收藏。', '佛教法器, 金刚杵, 佛铃, 藏传佛教', '2025-05-28 03:00:22.485432', '2025-05-28 03:00:22.485432');
INSERT INTO "public"."product_categories" VALUES ('8ee2997b-2ce5-40b7-a116-5e420ae3391b', '蛇年2025', 'YEAR_OF_THE_SNAKE_2025', '2025蛇年主题珠宝系列，融合传统生肖元素与现代设计，展现灵动与智慧，为生肖年份增添特别纪念意义，成为新年礼物与自我表达的理想选择。', '792e259e-713e-4f1a-9bd5-1b84c3567ff9', 'LEVEL_2', NULL, NULL, 't', 'f', 10, '蛇年2025珠宝 - 生肖主题的灵动设计', '探索2025蛇年主题珠宝系列，融合传统生肖元素与现代设计。每件作品精心打造蛇的灵动形态，采用多种材质如宝石、金属、木材等呈现独特风格。蛇象征智慧、重生与变革，在东方文化中具有深厚意义。这些珠宝不仅是新年的完美礼物，更是佩戴者个性与文化传承的表达。无论是手链、项链还是戒指，都能为您的装扮增添特别的生肖年份纪念意义，展现独特魅力与文化自信，成为新年期间的话题焦点与时尚亮点。', '蛇年珠宝, 生肖饰品, 2025趋势, 智慧象征', '2025-05-28 03:00:22.486431', '2025-05-28 03:00:22.486431');
INSERT INTO "public"."product_categories" VALUES ('9098463d-e301-426e-9519-adbe7540adb9', '红绳', 'RED_STRING', '流行红绳珠宝系列，以简约设计与文化寓意著称，象征保护与好运，展现东方美学，为日常佩戴带来一抹亮色与积极能量。', '792e259e-713e-4f1a-9bd5-1b84c3567ff9', 'LEVEL_2', NULL, NULL, 't', 'f', 20, '红绳珠宝 - 传统保护的能量饰品', '浏览红绳珠宝系列，以简约设计与文化寓意著称。我们的红绳手链、项链等饰品采用优质红线编织，搭配各种宝石、金属坠饰，展现东方美学精髓。红绳在许多文化中象征保护、好运与积极能量，常用于驱邪避灾、祈求平安。这些珠宝适合日常佩戴，为您的装扮增添一抹亮色，同时传递美好寓意。无论是自用还是赠送亲友，红绳珠宝都是表达祝福与关怀的理想选择，连接传统智慧与现代时尚。', '红绳珠宝, 保护饰品, 东方文化, 好运象征', '2025-05-28 03:00:22.487937', '2025-05-28 03:00:22.487937');
INSERT INTO "public"."product_categories" VALUES ('5011327d-fdb3-4e9e-ba67-340e39307160', '上衣', 'TOP_WOMEN', '女士舒适上衣系列，采用柔软面料与精致剪裁，展现女性的柔美与优雅，适合多种场合穿着，成为衣橱中的百搭单品，彰显自然气质。', 'ba8caffe-dd48-4fe2-9cc8-3a9a3abfdd5a', 'LEVEL_3', NULL, NULL, 't', 'f', 120, '女士舒适上衣 - 柔美优雅的日常选择', '女士舒适上衣系列，采用柔软面料与精致剪裁制作。我们的上衣款式多样，包括宽松T恤、修身衬衫、柔软针织衫等，展现女性的柔美与优雅。面料选择注重透气性与舒适度，适合日常穿着、冥想练习或休闲出行。每款上衣都经过精心设计，细节处理考究，能够轻松搭配各种下装，成为衣橱中的百搭单品。无论是追求休闲风格还是优雅气质，都能找到适合的选择，彰显自然气质与个性魅力。', '女士上衣, 舒适面料, 精致剪裁, 百搭配饰', '2025-05-28 03:00:22.50716', '2025-05-28 03:00:22.50716');
INSERT INTO "public"."product_categories" VALUES ('f3857cd3-cfac-4127-add2-11be4fbddbed', '翡翠项链', 'JADE_NECKLACE', '精选翡翠项链系列，展现宝石的温润光泽与高贵气质，融合传统工艺与现代设计，成为彰显品味与传承文化的理想饰品，适合各种重要场合。', '792e259e-713e-4f1a-9bd5-1b84c3567ff9', 'LEVEL_2', NULL, NULL, 't', 'f', 30, '翡翠项链 - 温润高贵的东方宝石', '探索精选翡翠项链系列，展现宝石的温润光泽与高贵气质。我们提供多种款式，从传统珠串到现代镶嵌设计，每件作品都采用优质翡翠制作，确保颜色纯正与质地细腻。翡翠在东方文化中象征繁荣、长寿与高贵，佩戴翡翠项链不仅是时尚选择，更是文化传承与品味彰显的方式。这些项链适合正式场合、礼品赠送以及日常珍藏，为您的装扮增添优雅气质，成为传递东方美学与个人风格的完美配饰。', '翡翠项链, 东方宝石, 高贵饰品, 传统工艺', '2025-05-28 03:00:22.488943', '2025-05-28 03:00:22.488943');
INSERT INTO "public"."product_categories" VALUES ('3efb29e7-2d0c-4a99-9c0e-02f804586afd', '翡翠手链', 'JADE_BRACELET', '精美翡翠手链系列，展现宝石的自然纹理与优雅色泽，结合舒适佩戴体验，成为日常搭配与礼物赠送的理想选择，传递美好寓意与文化价值。', '792e259e-713e-4f1a-9bd5-1b84c3567ff9', 'LEVEL_2', NULL, NULL, 't', 'f', 40, '翡翠手链 - 自然纹理的优雅配饰', '浏览精美翡翠手链系列，展现宝石的自然纹理与优雅色泽。我们的手链采用优质翡翠制作，款式多样，包括珠串、镶嵌、雕刻等多种形式。翡翠手链不仅美观大方，还具有良好的佩戴舒适度，适合日常搭配各种风格装扮。在东方文化中，翡翠象征纯洁、平安与和谐，是赠送亲友表达祝福的理想选择。每件作品都经过精心打磨与质量检验，确保光泽持久、结构牢固，成为您珠宝收藏中的经典之选，传递美好寓意与文化价值。', '翡翠手链, 自然宝石, 优雅配饰, 平安象征', '2025-05-28 03:00:22.488943', '2025-05-28 03:00:22.488943');
INSERT INTO "public"."product_categories" VALUES ('b2532dc7-306d-436c-85ea-920f2becd4e5', '佛陀手链', 'BUDDHA_BRACELET', '佛陀形象手链系列，以庄严佛像传递智慧与慈悲，展现宗教文化的深厚底蕴，为佩戴者带来心灵安宁与精神寄托，成为信仰表达与日常佩戴的理想结合。', '792e259e-713e-4f1a-9bd5-1b84c3567ff9', 'LEVEL_2', NULL, NULL, 't', 'f', 50, '佛陀手链 - 智慧慈悲的精神配饰', '探索佛陀手链系列，以庄严佛像传递智慧与慈悲。我们提供多种佛像造型的手链，包括释迦牟尼、观音、弥勒等多种类型，采用金属、宝石、木质等材质精心制作。每尊佛像都经过细致雕刻，展现佛教文化的深厚底蕴。佩戴佛陀手链不仅是信仰表达的方式，更是心灵安宁与精神寄托的象征。这些手链适合日常佩戴、冥想辅助以及特殊场合，帮助您保持内心的平静与专注，连接佛教智慧与现代生活，成为精神修行与时尚风格的完美结合。', '佛陀手链, 佛像饰品, 智慧象征, 精神寄托', '2025-05-28 03:00:22.489941', '2025-05-28 03:00:22.489941');
INSERT INTO "public"."product_categories" VALUES ('e436becc-4632-4c9b-865b-e52eeaa4d823', '佛陀项链', 'BUDDHA_NECKLACE', '精致佛陀项链系列，以佛像吊坠展现宗教艺术之美，融合传统工艺与现代设计，为佩戴者带来精神力量与文化认同，成为表达信仰与个人风格的独特饰品。', '792e259e-713e-4f1a-9bd5-1b84c3567ff9', 'LEVEL_2', NULL, NULL, 't', 'f', 60, '佛陀项链 - 宗教艺术的精神饰品', '浏览精致佛陀项链系列，以佛像吊坠展现宗教艺术之美。我们的项链采用优质材料如纯银、黄金、宝石等制作，佛像造型精美，细节丰富，展现不同佛教传统的艺术风格。每件作品都经过工匠精心打磨，确保质感与光泽。佛陀项链不仅是信仰表达的载体，更是个人风格的独特展现。它们适合日常佩戴、宗教仪式以及礼品赠送，帮助佩戴者连接佛教智慧，获得精神力量。通过佩戴佛像，您可以随时提醒自己实践慈悲与智慧，将宗教文化融入日常生活，成为内外和谐的象征。', '佛陀项链, 宗教饰品, 佛像珠宝, 文化传承', '2025-05-28 03:00:22.489941', '2025-05-28 03:00:22.489941');
INSERT INTO "public"."product_categories" VALUES ('b388fe53-5dd0-4a86-b99c-c4c5533637d3', '龙', 'DRAGON', '龙主题珠宝系列，展现东方神话的威严与力量，融合传统图案与现代设计，为佩戴者带来勇气与繁荣寓意，成为独特文化表达与时尚声明的理想选择。', '792e259e-713e-4f1a-9bd5-1b84c3567ff9', 'LEVEL_2', NULL, NULL, 't', 'f', 70, '龙珠宝 - 权力与繁荣的东方象征', '探索龙主题珠宝系列，展现东方神话的威严与力量。我们的龙形手链、项链、戒指等饰品采用精细工艺制作，呈现龙的灵动姿态与华丽细节。龙在东方文化中象征权力、繁荣与好运，是皇室与尊贵的代表。这些珠宝融合传统图案与现代设计，适合各种场合佩戴，展现独特文化表达。无论是追求时尚个性还是表达文化自豪感，龙珠宝都能成为引人注目的焦点，传递积极能量与高贵气质。每件作品都经过严格质量控制，确保材质优良与工艺精湛，成为您珠宝收藏中的珍品。', '龙珠宝, 权力象征, 繁荣寓意, 东方神话', '2025-05-28 03:00:22.490943', '2025-05-28 03:00:22.490943');
INSERT INTO "public"."product_categories" VALUES ('4db72b73-948b-4748-afc9-595fa95dc3f1', '手镯', 'CUFF_BANGLE', '时尚手镯系列，展现大胆设计与材质多样性，从金属光泽到宝石镶嵌，为腕间增添个性与魅力，成为表达自我风格与场合搭配的理想配饰。', '792e259e-713e-4f1a-9bd5-1b84c3567ff9', 'LEVEL_2', NULL, NULL, 't', 'f', 80, '手镯 - 大胆设计的腕间时尚', '浏览时尚手镯系列，展现大胆设计与材质多样性。我们的手镯包括宽边手镯、细手环、镶嵌宝石手镯等多种款式，采用黄金、白金、玫瑰金、宝石等优质材料制作。手镯设计从简约现代到复古华丽，满足不同个性与场合需求。佩戴手镯能够为您的腕间增添个性与魅力，成为整体造型的点睛之笔。无论是单独佩戴还是多层叠搭，都能展现独特的时尚态度。我们提供多种尺寸与调节方式，确保舒适贴合，让时尚与舒适并存，成为日常穿搭与特殊场合的理想配饰。', '时尚手镯, 腕间配饰, 金属光泽, 宝石镶嵌', '2025-05-28 03:00:22.490943', '2025-05-28 03:00:22.490943');
INSERT INTO "public"."product_categories" VALUES ('4f5348d7-4cc5-45bf-b2fc-b11c0aca9905', '925/999银', '925_999_SILVER', '高品质银饰系列，采用纯银材质制作，展现银的纯净光泽与精致工艺，提供多样款式选择，从简约到华丽，满足不同风格需求，是日常佩戴与礼物赠送的理想选择。', '792e259e-713e-4f1a-9bd5-1b84c3567ff9', 'LEVEL_2', NULL, NULL, 't', 'f', 90, '925/999银饰 - 纯净光泽的精致珠宝', '探索高品质银饰系列，采用925纯银或999足银精心制作。我们的银饰包括项链、手链、戒指、耳环等多种类型，设计风格从简约现代到复古民族，满足不同审美需求。银饰以其纯净光泽与亲和力著称，不易引起过敏，适合长期佩戴。每件作品都经过精细打磨与质量检验，确保光泽持久、结构牢固。银饰不仅是时尚选择，更具有投资收藏价值，尤其是限量版与手工制作款式。无论是日常穿搭、特殊场合还是作为礼物，银饰都能展现佩戴者的品味与风格，传递纯洁、真诚的美好寓意，成为珠宝收藏中的重要类别。', '纯银饰品, 高品质银饰, 纯净光泽, 手工制作', '2025-05-28 03:00:22.491949', '2025-05-28 03:00:22.491949');
INSERT INTO "public"."product_categories" VALUES ('a80a2ae9-814d-4577-8f23-ea959c891462', '藏式手链', 'TIBETAN_BRACELET', '精美藏式手链系列，采用传统工艺与天然材料制作，展现独特的民族风格与神秘魅力，成为表达个性与文化认同的理想配饰。', 'c2602244-50d1-43f0-b2a5-5929baa487e0', 'LEVEL_2', NULL, NULL, 't', 'f', 10, '藏式手链 - 民族风格的神秘魅力', '探索精美藏式手链系列，采用传统工艺与天然材料精心制作。这些手链融合藏族独特设计元素，如多彩珠串、金属雕花、佛像图案等，展现浓郁的民族风格与神秘魅力。每件作品都由经验丰富的工匠手工完成，确保细节精致与品质优良。藏式手链不仅是时尚配饰，更承载着藏族人民的信仰与祝福，适合日常佩戴、文化活动或作为礼物赠送，成为表达个性与文化认同的理想选择，为您的装扮增添独特的异域风情。', '藏式手链, 民族饰品, 传统工艺, 佛像图案', '2025-05-28 03:00:22.496948', '2025-05-28 03:00:22.496948');
INSERT INTO "public"."product_categories" VALUES ('b2f1bb92-99c6-43b6-97ef-20dca3f4165d', '999黄金珠宝', '999_GOLD_JEWELRY', '奢华黄金珠宝系列，采用999足金制作，展现黄金的高贵色泽与精湛工艺，融合传统与现代设计，成为财富象征与珍贵礼物的完美结合，适合投资收藏与重要场合佩戴。', '792e259e-713e-4f1a-9bd5-1b84c3567ff9', 'LEVEL_2', NULL, NULL, 't', 'f', 100, '999黄金珠宝 - 贵族色调的投资珍品', '浏览奢华黄金珠宝系列，采用999足金精心制作。我们的黄金珠宝包括项链、手链、戒指、耳环、吊坠等多种类型，设计风格从传统福禄寿到现代简约，满足不同文化背景与时尚需求。黄金以其保值增值特性著称，是财富与地位的象征。每件作品都经过精密铸造与细致打磨，确保黄金纯净度与光泽度。黄金珠宝不仅是珍贵礼物的选择，更是财富传承与投资收藏的理想载体。无论是婚庆喜事、节日馈赠还是个人珍藏，黄金珠宝都能展现佩戴者的尊贵气质，传递永恒的价值与美好祝福，成为家族财富与文化传承的重要象征。', '黄金珠宝, 贵族色调, 投资收藏, 保值增值', '2025-05-28 03:00:22.492948', '2025-05-28 03:00:22.492948');
INSERT INTO "public"."product_categories" VALUES ('616bd56e-606f-4c49-9e51-491fd6f2bb65', '狐狸珠宝', 'FOX_JEWELRY', '狐狸主题珠宝系列，以灵动造型展现智慧与神秘，融合宝石镶嵌与金属工艺，成为时尚潮流中的独特单品，吸引追求个性与故事性饰品的佩戴者。', '792e259e-713e-4f1a-9bd5-1b84c3567ff9', 'LEVEL_2', NULL, NULL, 't', 'f', 110, '狐狸珠宝 - 智慧神秘的时尚单品', '探索狐狸主题珠宝系列，以灵动造型展现智慧与神秘。我们的狐狸珠宝包括项链、耳环、手链等多种款式，采用黄金、白金、宝石等优质材料制作。狐狸形象通过精细雕刻与镶嵌工艺呈现，细节丰富，栩栩如生。在许多文化中，狐狸象征智慧、机敏、神秘与魅力，这些特质通过珠宝设计传递给佩戴者。狐狸珠宝适合追求个性表达与时尚潮流的人士，成为引人注目的配饰。无论是日常穿搭还是特殊场合，都能为您的装扮增添独特风格与话题性，展现非凡品味与个性魅力，成为珠宝收藏中的创意之选。', '狐狸饰品, 智慧象征, 神秘魅力, 个性珠宝', '2025-05-28 03:00:22.492948', '2025-05-28 03:00:22.492948');
INSERT INTO "public"."product_categories" VALUES ('50696737-a64a-4761-94b6-c3224dabd486', '铜手链', 'COPPER_BRACELET', '纯铜手链系列，利用铜的自然能量与健康益处，展现复古质感与耐用特性，为佩戴者带来时尚与功能性兼具的腕间装饰，是追求自然疗法与复古风格的理想选择。', '792e259e-713e-4f1a-9bd5-1b84c3567ff9', 'LEVEL_2', NULL, NULL, 't', 'f', 120, '铜手链 - 自然能量的复古健康饰品', '浏览纯铜手链系列，利用铜的自然能量与健康益处。我们的铜手链设计多样，包括编织手链、宽边手镯、镶嵌宝石款式等，展现复古质感与耐用特性。铜在传统医学中被认为具有抗炎、能量平衡等功效，佩戴铜手链成为自然疗法的实践方式。这些手链适合追求健康生活方式与复古风格的人士，为腕间增添独特装饰。铜材经过特殊处理，防止氧化变色，长期佩戴依然保持光泽。无论是单独佩戴还是与其他手链叠搭，铜手链都能展现个性魅力，成为连接自然元素与时尚风格的理想选择，特别适合户外爱好者与健康追求者。', '铜手链, 自然疗法, 复古风格, 健康饰品', '2025-05-28 03:00:22.493941', '2025-05-28 03:00:22.493941');
INSERT INTO "public"."product_categories" VALUES ('1b0946ee-35c6-470f-b72e-817d02091bcd', '收藏品', 'COLLECTABLE_ITEMS', '珍贵珠宝收藏品系列，包括限量版设计、古董珠宝与稀有宝石作品，展现卓越工艺与历史价值，为收藏家与鉴赏家提供独特投资与审美体验。', '792e259e-713e-4f1a-9bd5-1b84c3567ff9', 'LEVEL_2', NULL, NULL, 't', 'f', 130, '珠宝收藏品 - 珍贵工艺的历史见证', '探索珍贵珠宝收藏品系列，包括限量版设计、古董珠宝与稀有宝石作品。我们的收藏品来自世界各地的知名设计师、皇家御用珠宝商以及历史拍卖会，每件作品都经过专业鉴定与认证，确保其真实性和历史价值。这些珠宝展现不同历史时期的工艺风格，从文艺复兴到装饰艺术时代，为收藏家与鉴赏家提供独特的审美体验。限量版作品则融合现代设计与传统工艺，数量稀缺，具有高度收藏价值。无论是作为投资、传承还是纯粹欣赏，珠宝收藏品都是珍贵的文化遗产与财富象征，帮助您建立具有个性与深度的收藏系列，传承家族文化与艺术品味。', '珠宝收藏品, 限量版设计, 古董珠宝, 稀有宝石', '2025-05-28 03:00:22.493941', '2025-05-28 03:00:22.493941');
INSERT INTO "public"."product_categories" VALUES ('d93f22af-8151-4358-8dff-264b123fa6be', '十二星座系列', '12_CONSTELLATIONS_SERIES', '星座主题珠宝系列，融合天文学元素与个人星象特征，通过宝石色彩与符号设计展现独特个性，为佩戴者带来与生辰相关的神秘连接与时尚表达。', '792e259e-713e-4f1a-9bd5-1b84c3567ff9', 'LEVEL_2', NULL, NULL, 't', 'f', 140, '十二星座珠宝 - 神秘星象的时尚表达', '浏览星座主题珠宝系列，融合天文学元素与个人星象特征。我们的十二星座珠宝包括项链、戒指、耳环等多种类型，每件作品根据星座符号、守护星、幸运石等元素进行设计，采用对应色彩的宝石与金属工艺呈现。佩戴星座珠宝不仅是一种时尚表达，更是一种与生辰星象的神秘连接，展现佩戴者的个性特质与宇宙能量。这些珠宝适合星座爱好者、占星学研究者以及追求个性化配饰的人士，成为话题焦点与情感寄托。无论是自用还是作为生日礼物，星座珠宝都能传递特别的寓意，连接个人命运与宇宙奥秘，展现独特的时尚品味与精神追求。', '星座珠宝, 星象符号, 守护石, 个性配饰', '2025-05-28 03:00:22.494941', '2025-05-28 03:00:22.494941');
INSERT INTO "public"."product_categories" VALUES ('6bc7b47e-4179-4cf2-a5bb-c4ea090ef297', '皮革手链', 'LEATHER_BRACELETS', '时尚皮革手链系列，结合柔软材质与金属装饰，展现随性与酷感风格，为腕间增添不羁魅力，是追求休闲与个性表达的理想配饰，适合多种场合搭配。', '792e259e-713e-4f1a-9bd5-1b84c3567ff9', 'LEVEL_2', NULL, NULL, 't', 'f', 150, '皮革手链 - 随性酷感的个性腕饰', '探索时尚皮革手链系列，结合柔软优质皮革与金属装饰。我们的皮革手链提供多种颜色、宽度与扣环设计，展现随性与酷感风格。皮革材质经过特殊处理，确保耐用性与舒适佩戴体验。金属装饰如吊坠、链条、铆钉等增加细节亮点，提升整体设计感。皮革手链适合追求休闲风格与个性表达的人士，能够为腕间增添不羁魅力。无论是搭配牛仔装、休闲衫还是时尚外套，都能展现独特风格。我们提供男女款式选择，每件作品都经过精细制作，确保质量与质感，成为日常穿搭与个性展示的理想配饰，展现自由不羁的生活态度。', '皮革手链, 酷感配饰, 休闲风格, 个性表达', '2025-05-28 03:00:22.494941', '2025-05-28 03:00:22.494941');
INSERT INTO "public"."product_categories" VALUES ('62ce3ff8-fe78-4775-80c4-9ab23844def4', '金属系列', 'METAL_SERIES', '金属主题珠宝系列，突出金属本身的质感与光泽，通过锻造、雕刻等工艺展现力量与现代美感，为佩戴者带来强硬与优雅并存的风格选择，成为前卫时尚与经典设计的代表。', '792e259e-713e-4f1a-9bd5-1b84c3567ff9', 'LEVEL_2', NULL, NULL, 't', 'f', 160, '金属珠宝 - 质感光泽的现代力量', '浏览金属主题珠宝系列，突出金属本身的质感与光泽。我们的金属珠宝包括纯银、黄金、玫瑰金、钛钢等多种材质，通过锻造、雕刻、抛光等工艺展现力量与现代美感。这些珠宝设计从简约几何到复杂雕塑风格，适合追求前卫时尚与经典设计的人士。金属珠宝能够为佩戴者带来强硬与优雅并存的风格，成为整体造型的亮点。每件作品都经过精心制作，确保金属纯度与工艺质量。无论是日常佩戴还是特殊场合，金属珠宝都能展现独特的时尚态度，传递现代审美与个性力量，成为珠宝收藏中的经典与前卫之选，永不过时且引人注目。', '金属珠宝, 质感光泽, 现代设计, 力量美感', '2025-05-28 03:00:22.495944', '2025-05-28 03:00:22.495944');
INSERT INTO "public"."product_categories" VALUES ('10df813e-1b02-49d5-8389-0915c992c53c', '藏式念珠与项链', 'TIBETAN_MALA_NECKLACE', '藏式念珠与项链系列，结合宗教元素与时尚设计，用于修行与日常佩戴，展现精神信仰与审美风格的完美融合，是连接内心与文化的桥梁。', 'c2602244-50d1-43f0-b2a5-5929baa487e0', 'LEVEL_2', NULL, NULL, 't', 'f', 20, '藏式念珠与项链 - 信仰与时尚的结合', '浏览藏式念珠与项链系列，结合宗教元素与时尚设计。我们的念珠采用优质木材、宝石、珊瑚等材料制作，颗数遵循传统如108颗、21颗等，适合修行计数与冥想使用。项链则融合佛像、经文、幸运符等元素，设计风格从传统到现代简约。这些饰品不仅是修行工具，更是时尚配饰，展现佩戴者的精神信仰与审美品味。每件作品都经过僧侣加持与能量赋予，确保其神圣性与文化价值。适合宗教仪式、日常佩戴或作为珍贵礼物，帮助您连接内心平静与藏族文化，成为精神修行与时尚表达的双重象征。', '藏式念珠, 念珠项链, 修行工具, 宗教饰品', '2025-05-28 03:00:22.497948', '2025-05-28 03:00:22.497948');
INSERT INTO "public"."product_categories" VALUES ('c5f96dac-d07a-4a7f-91ad-28e06c216215', '藏式戒指', 'TIBETAN_RING', '独特藏式戒指系列，以大胆设计与象征符号展现个性，采用金属与宝石制作，融合传统工艺与现代审美，成为手指间的文化表达与力量象征。', 'c2602244-50d1-43f0-b2a5-5929baa487e0', 'LEVEL_2', NULL, NULL, 't', 'f', 30, '藏式戒指 - 大胆设计的文化象征', '探索独特藏式戒指系列，以大胆设计与象征符号展现个性。我们的戒指采用优质金属如银、金、铜等制作，镶嵌宝石、珊瑚、松石等珍贵材料，呈现藏族传统图案如八宝、六字真言、佛像等。每枚戒指都经过精细雕刻与手工打磨，确保佩戴舒适与品质优良。藏式戒指不仅是时尚饰品，更承载着祝福、保护、智慧等象征意义，适合各种场合佩戴，成为手指间的文化表达与力量象征。无论是追求个性风格还是文化传承，这些戒指都能为您的装扮增添独特魅力，传递深厚的精神内涵。', '藏式戒指, 象征符号, 传统图案, 金属宝石', '2025-05-28 03:00:22.497948', '2025-05-28 03:00:22.497948');
INSERT INTO "public"."product_categories" VALUES ('4aeb9171-2dce-486e-b586-9f7536c8e889', '藏式唱钵', 'TIBETAN_SINGING_BOWLS', '传统藏式唱钵系列，以青铜合金打造，通过敲击产生和谐振动，用于冥想、疗愈与仪式，帮助平衡能量，创造神圣氛围，是声音疗愈的理想工具。', 'c2602244-50d1-43f0-b2a5-5929baa487e0', 'LEVEL_2', NULL, NULL, 't', 'f', 40, '藏式唱钵 - 和谐振动的冥想工具', '浏览传统藏式唱钵系列，以青铜合金精心打造。这些唱钵通过敲击或摩擦产生深沉和谐的振动，频率独特，用于冥想、声音疗愈、能量净化等多种修行方式。藏式唱钵在佛教仪式中具有重要地位，帮助修行者集中注意力、平衡身心能量、进入深度冥想状态。我们的唱钵经过严格挑选，确保音质纯净、振动持久。每只唱钵都附带专用木槌与使用指南，适合初学者与专业人士使用。无论是个人修行、疗愈工作坊还是家居能量维护，藏式唱钵都能为您创造神圣氛围，带来身心和谐与内在平静，成为声音疗愈领域的珍贵工具。', '藏式唱钵, 声音疗愈, 冥想工具, 能量平衡', '2025-05-28 03:00:22.497948', '2025-05-28 03:00:22.497948');
INSERT INTO "public"."product_categories" VALUES ('f39d7472-164b-4860-b4c7-51e0b00684cb', '藏式经幡', 'TIBETAN_PRAYER_FLAGS', '彩色藏式经幡系列，印有经文与吉祥图案，随风飘动传播祝福与正能量，用于装饰与祈福，为环境增添神圣氛围与文化美感。', 'c2602244-50d1-43f0-b2a5-5929baa487e0', 'LEVEL_2', NULL, NULL, 't', 'f', 50, '藏式经幡 - 随风传播的吉祥祝福', '探索彩色藏式经幡系列，印有传统经文与吉祥图案。这些经幡采用优质布料制作，色彩鲜艳持久，图案包括佛教经文、佛像、神兽等，具有祈福、驱邪、传播正能量的寓意。经幡在藏族文化中象征神圣的祈祷，随风飘动时 believed to spread spiritual messages and blessings。我们的经幡提供多种尺寸与长度选择，适合家居装饰、庭院布置、旅行纪念或宗教仪式。悬挂经幡不仅为环境增添神圣氛围与文化美感，更是一种参与藏族精神实践的方式，为生活空间带来和谐与安宁，传递美好的愿望与祝福。', '藏式经幡, 经文图案, 吉祥祝福, 家居装饰', '2025-05-28 03:00:22.499159', '2025-05-28 03:00:22.499159');
INSERT INTO "public"."product_categories" VALUES ('8093514d-3e58-45cc-812f-1c4b04f9c904', '藏式转经筒', 'TIBETAN_PRAYER_WHEELS', '藏式转经筒系列，内藏经文，通过旋转积累功德，用于个人修行与祈福，展现精美的工艺与深厚的宗教意义，是藏传佛教的重要法器。', 'c2602244-50d1-43f0-b2a5-5929baa487e0', 'LEVEL_2', NULL, NULL, 't', 'f', 60, '藏式转经筒 - 旋转积累功德的法器', '浏览藏式转经筒系列，内藏大量经文，通过旋转积累功德与祈福。我们的转经筒采用优质木材、金属、皮革等材料制作，设计从手持小型到大型庭院装饰多种类型。每个转经筒都经过僧侣加持，确保其宗教意义与灵性价值。在藏传佛教中，转经筒代表佛法的传播与修行的实践，旋转一圈相当于诵读内部所有经文。这些法器适合个人修行、家居装饰、寺庙供奉或作为珍贵礼物。无论是手持念经还是庭院陈设，转经筒都能为您的生活空间带来神圣氛围，成为连接物质世界与精神领域的桥梁，传递无尽的祝福与智慧。', '藏式转经筒, 经文法器, 功德积累, 宗教意义', '2025-05-28 03:00:22.50016', '2025-05-28 03:00:22.50016');
INSERT INTO "public"."product_categories" VALUES ('f7ff8396-f88d-49db-b1f2-dc6fad6fe96f', '藏式铜铃', 'TIBETAN_TINGSHA BELLS', '传统藏式铜铃系列，以纯铜打造，发出清脆声音用于修行与仪式，象征智慧与慈悲的结合，帮助集中注意力，创造神圣庄严的氛围。', 'c2602244-50d1-43f0-b2a5-5929baa487e0', 'LEVEL_2', NULL, NULL, 't', 'f', 70, '藏式铜铃 - 清脆声音的修行辅助', '探索传统藏式铜铃系列，以纯铜精心打造。这些铜铃设计精美， often featuring dragon and other auspicious symbols, 发出清脆悠扬的声音，用于冥想、祈祷、仪式等多种修行场合。在藏传佛教中，铜铃象征智慧（空性）与慈悲（方法）的完美结合，帮助修行者集中注意力、净化空间、驱散干扰。我们的铜铃提供多种尺寸与声音选择，适合个人修行、寺庙仪式或家居能量净化。每个铜铃都经过精细调试，确保音质纯净、声音传播远。使用铜铃不仅能增强修行效果，更是连接古老智慧与现代精神实践的方式，为您的修行之旅增添传统力量与文化深度。', '藏式铜铃, 修行辅助, 智慧慈悲, 仪式法器', '2025-05-28 03:00:22.501159', '2025-05-28 03:00:22.501159');
INSERT INTO "public"."product_categories" VALUES ('2445fe19-b637-4d6c-898d-4824651278f6', '唐卡', 'THANGKA_PAINTINGS', '传统唐卡绘画系列，以矿物颜料绘制佛像与藏族神话，展现精湛的绘画技艺与深厚的精神内涵，是藏族艺术的珍品，具有收藏与装饰价值。', 'c2602244-50d1-43f0-b2a5-5929baa487e0', 'LEVEL_2', NULL, NULL, 't', 'f', 80, '唐卡绘画 - 藏族艺术的精神珍品', '浏览传统唐卡绘画系列，以矿物颜料精心绘制佛像与藏族神话场景。我们的唐卡由经验丰富的画师手工制作，遵循千年传统工艺，使用金箔、银箔、宝石粉末等珍贵材料，确保色彩鲜艳持久、线条细腻流畅。每幅唐卡都蕴含深厚的宗教意义与精神价值，展现佛菩萨的神圣形象与藏族宇宙观。唐卡不仅是艺术品，更是修行辅助工具，帮助观想与冥想。我们提供多种尺寸与题材选择，包括佛像、菩萨、护法、本尊等，适合家居供奉、寺庙装饰或艺术收藏。每幅唐卡都附有详细背景说明与保养指南，帮助您深入了解其文化内涵，珍藏这份来自雪域高原的艺术瑰宝，为生活空间带来神圣氛围与文化深度。', '唐卡绘画, 藏族艺术, 佛像唐卡, 艺术收藏', '2025-05-28 03:00:22.502161', '2025-05-28 03:00:22.502161');
INSERT INTO "public"."product_categories" VALUES ('a10e684e-553f-4200-9f07-311dbead4a88', '藏式天珠', 'TIBETAN_DZI_BEADS', '珍贵藏式天珠系列，采用天然石头与神秘工艺制作，蕴含古老传说与保护能量，展现独特纹理与神秘魅力，是收藏与佩戴的理想选择。', 'c2602244-50d1-43f0-b2a5-5929baa487e0', 'LEVEL_2', NULL, NULL, 't', 'f', 90, '藏式天珠 - 神秘纹理的保护宝石', '探索珍贵藏式天珠系列，采用天然石头与古老神秘工艺制作。天珠以其独特的纹理、眼数与图案著称， each pattern carrying specific spiritual significance and protective qualities。在藏族文化中，天珠被视为吉祥物，能够驱邪避灾、带来好运、增强能量。我们的天珠经过严格鉴定，确保其 authenticity and quality，提供多种款式如单珠、手串、项链等。天珠适合收藏、佩戴或作为珍贵礼物，其神秘魅力与文化价值使其成为珠宝爱好者与文化探索者的理想选择。每颗天珠都附有详细图案解释与保养说明，帮助您深入理解其内涵，体验古老智慧的现代传承。', '藏式天珠, 保护宝石, 神秘纹理, 文化传承', '2025-05-28 03:00:22.503162', '2025-05-28 03:00:22.503162');
INSERT INTO "public"."product_categories" VALUES ('2ffc2508-b703-4831-9c0b-f96b5c5539dd', '藏式衣物与围巾', 'TIBETAN_CLOTHES_SCARVES', '藏式传统衣物与围巾系列，采用厚实面料与鲜艳色彩，展现民族风情，提供保暖与舒适，是体验藏族生活的理想服饰，适合旅行与特殊场合。', 'c2602244-50d1-43f0-b2a5-5929baa487e0', 'LEVEL_2', NULL, NULL, 't', 'f', 100, '藏式衣物与围巾 - 民族风情的保暖选择', '浏览藏式传统衣物与围巾系列，采用厚实面料如羊毛、牦牛绒、棉布等制作，色彩鲜艳，图案充满民族风情。我们的衣物包括藏袍、衬衫、帽子等多种类型，围巾则提供多种尺寸与佩戴方式，展现藏族独特的审美与文化特色。这些服饰不仅美观大方，更具有出色的保暖性能与舒适度，适合高原气候与各种户外活动。穿着藏式衣物与围巾，您将深入体验藏族生活方式，成为文化传承的一部分。我们的产品适合旅行者、文化活动参与者或寻求独特风格的人士，为日常装扮增添异域魅力，成为连接传统与现代的时尚桥梁。', '藏式衣物, 民族服饰, 保暖围巾, 传统风格', '2025-05-28 03:00:22.504162', '2025-05-28 03:00:22.504162');
INSERT INTO "public"."product_categories" VALUES ('4d78477c-c274-42c5-8838-9d9a8cb206e2', '藏式海螺', 'TIBETAN_CONCH_SHELL', '藏式海螺系列，作为佛教重要法器，用于仪式与冥想，其声音象征佛法传播，帮助净化空间，增强修行氛围，展现神圣的文化意义与实用价值。', 'c2602244-50d1-43f0-b2a5-5929baa487e0', 'LEVEL_2', NULL, NULL, 't', 'f', 110, '藏式海螺 - 法音传播的神圣法器', '探索藏式海螺系列，作为佛教重要的法器之一。这些海螺采用天然大螺精心打磨，开口发出宏亮声音，声音被认为能净化空间、驱散邪恶、传播佛法。在藏传佛教中，海螺象征佛陀的教法传播与胜利之声，常用于宗教仪式、冥想引导与祈祷活动中。我们的海螺提供多种尺寸与装饰选择，包括简单原生态与镶嵌宝石、金属雕刻等华丽款式。每个海螺都附有使用指南与文化背景说明，确保您正确使用其功能与含义。无论是用于个人修行、寺庙仪式还是家居能量净化，藏式海螺都能为您的精神实践增添神圣氛围，成为连接古老智慧与现代修行的珍贵桥梁，传递和平与觉醒的力量。', '藏式海螺, 法器海螺, 净化空间, 佛法传播', '2025-05-28 03:00:22.504162', '2025-05-28 03:00:22.504162');
INSERT INTO "public"."product_categories" VALUES ('ba8caffe-dd48-4fe2-9cc8-3a9a3abfdd5a', '女士', 'WOMEN', '女士专属服装系列，包括冥想、瑜伽、日常穿着等多种款式，展现优雅与舒适，为现代女性提供全方位的穿着选择，彰显自然气质与个性风格。', '00e865af-c686-404a-8760-dbb3bca5ecbc', 'LEVEL_2', NULL, NULL, 't', 'f', 10, '女士冥想与瑜伽服装', '女士专属服装系列，专为冥想、瑜伽和日常穿着设计。我们的女士服装采用贴合女性身形的剪裁，使用柔软透气的天然面料，展现优雅与舒适。款式多样，从宽松的冥想长袍到修身的瑜伽裤，从休闲的佛系T恤到优雅的连衣裙，满足不同场合需求。每件作品都融合传统元素与现代设计，彰显自然气质与个性风格，帮助现代女性在繁忙生活中保持内心平静与外在美丽。', '女士冥想服装, 瑜伽裤, 佛系T恤, 休闲连衣裙', '2025-05-28 03:00:22.506167', '2025-05-28 03:00:22.506167');
INSERT INTO "public"."product_categories" VALUES ('7be43317-35eb-418e-a0da-292c8b67b49d', '冥想瑜伽服', 'MEDITATION_QIGONG_CLOTHES_WOMEN', '专为女士设计的冥想瑜伽服装，采用宽松剪裁与柔软面料，确保舒适与自由移动，帮助深度放松与专注练习，展现优雅的修行姿态。', 'ba8caffe-dd48-4fe2-9cc8-3a9a3abfdd5a', 'LEVEL_3', NULL, NULL, 't', 'f', 100, '女士冥想瑜伽服 - 舒适与优雅的修行选择', '专为女士设计的冥想瑜伽服装系列，采用宽松剪裁与柔软面料制作。我们的服装确保舒适与自由移动，帮助您在练习中深度放松与专注。面料采用有机棉、竹纤维等天然材料，透气吸汗，适合各种瑜伽、冥想、气功练习。款式包括宽松长裤、舒适上衣、套装等多种选择，展现优雅的修行姿态。每件作品都经过精心设计，细节考究，为您的练习带来全方位的舒适体验，成为您精神实践的理想着装。', '女士瑜伽服, 冥想服装, 宽松长裤, 舒适上衣', '2025-05-28 03:00:22.506167', '2025-05-28 03:00:22.506167');
INSERT INTO "public"."product_categories" VALUES ('ad036486-f2c8-4be1-9c23-36def611da15', '佛系T恤', 'BUDDHA-INSPIRED_T-SHIRT_WOMEN', '女士佛系主题T恤，融合佛教元素与现代设计，采用优质棉料制作，展现精神内涵与时尚风格，成为日常穿着的理想选择，传递平和与智慧。', 'ba8caffe-dd48-4fe2-9cc8-3a9a3abfdd5a', 'LEVEL_3', NULL, NULL, 't', 'f', 110, '女士佛系T恤 - 精神内涵的时尚表达', '女士佛系主题T恤系列，融合佛教元素与现代设计。我们的T恤采用优质棉料制作，亲肤透气，版型修身。图案设计包括佛像、经文、莲花等多种宗教符号，展现精神内涵与艺术美感。这些T恤不仅是日常穿着的理想选择，更是表达个人信仰与追求平和的理想方式。每件作品都经过精心印刷，确保色彩鲜艳持久，图案细节清晰。适合各种场合穿着，为您的日常装扮增添文化深度与时尚风格，成为连接内心与外在的桥梁。', '佛系T恤, 佛教元素, 精神内涵, 日常穿着', '2025-05-28 03:00:22.50716', '2025-05-28 03:00:22.50716');
INSERT INTO "public"."product_categories" VALUES ('d109f10f-a9d9-465e-8a09-47df8e9fa1e0', '连衣裙', 'DRESS_WOMEN', '女士连衣裙系列，融合传统与现代设计，采用流畅面料制作，展现女性的优雅曲线与文化气质，适合多种场合穿着，成为时尚与舒适的完美结合。', 'ba8caffe-dd48-4fe2-9cc8-3a9a3abfdd5a', 'LEVEL_3', NULL, NULL, 't', 'f', 130, '女士连衣裙 - 优雅曲线的文化表达', '女士连衣裙系列，融合传统与现代设计元素。我们的连衣裙采用柔软流畅的面料制作，剪裁合身，展现女性的优雅曲线。款式包括宽松袍裙、修身包臀裙、层叠半身裙等多种风格，满足不同场合需求。设计细节融入文化元素如佛教图案、藏族色彩、东方美学等，展现独特的文化气质。每条连衣裙都经过精细制作，确保穿着舒适与品质优良。适合参加冥想活动、文化聚会、日常出行等场合，成为时尚与舒适的完美结合，让您在任何场合都能展现优雅与自信。', '女士连衣裙, 优雅曲线, 文化气质, 流畅面料', '2025-05-28 03:00:22.508166', '2025-05-28 03:00:22.508166');
INSERT INTO "public"."product_categories" VALUES ('d2be0199-66ee-4b0e-a94e-dc1611df8177', '外套', 'COATS_JACKETS_WOMEN', '女士外套系列，采用保暖面料与时尚设计，提供多种款式选择，从休闲夹克到优雅大衣，为不同季节与场合提供理想搭配，展现女性的独立与时尚态度。', 'ba8caffe-dd48-4fe2-9cc8-3a9a3abfdd5a', 'LEVEL_3', NULL, NULL, 't', 'f', 140, '女士外套 - 保暖与时尚的完美融合', '女士外套系列，采用高品质保暖面料与时尚设计制作。我们的外套款式多样，包括休闲夹克、连帽外套、修身大衣、皮草外套等，适合不同季节与场合穿着。设计注重细节，如精致刺绣、独特领口、功能性口袋等，展现女性的独立与时尚态度。外套不仅提供出色的保暖性能，更通过精心剪裁与时尚元素提升整体造型。无论是日常通勤、冥想旅行还是社交活动，都能找到理想的搭配，成为您衣橱中的必备单品，为您的装扮增添层次感与风格亮点。', '女士外套, 保暖夹克, 优雅大衣, 时尚设计', '2025-05-28 03:00:22.509297', '2025-05-28 03:00:22.509297');
INSERT INTO "public"."product_categories" VALUES ('4e5197d9-b8c8-4931-8c00-bef26f35a6b6', '女士长裤', 'PANTS_WOMEN', '女士长裤系列，采用舒适面料与修身剪裁，提供多种款式如哈伦裤、直筒裤、阔腿裤等，满足不同风格需求，为日常穿着与冥想练习提供理想选择，展现自然舒适与时尚风格。', 'ba8caffe-dd48-4fe2-9cc8-3a9a3abfdd5a', 'LEVEL_3', NULL, NULL, 't', 'f', 150, '女士长裤 - 舒适与风格的完美结合', '女士长裤系列，采用柔软舒适的面料与修身剪裁制作。我们的长裤款式丰富，包括哈伦裤、直筒裤、阔腿裤、瑜伽裤等，满足不同风格与需求。面料选择注重透气性与弹性，确保穿着舒适，适合日常穿着、冥想练习与各种活动。设计细节如高腰设计、宽松裤脚、精致腰带等，提升整体造型感。每条长裤都经过精细制作，确保版型稳定与品质优良。无论是追求休闲风格、运动装扮还是优雅气质，都能找到理想的款式，成为衣橱中的实用单品，展现自然舒适与时尚风格的完美结合。', '女士长裤, 舒适面料, 修身剪裁, 风格多样', '2025-05-28 03:00:22.509297', '2025-05-28 03:00:22.509297');
INSERT INTO "public"."product_categories" VALUES ('7dd2d24e-4c4a-4ec8-9fab-33064141dbda', '紧身裤', 'LEGGINGS_WOMEN', '女士紧身裤系列，采用高弹力面料制作，贴合身形，展现腿部线条，适合瑜伽、健身等运动场合，提供多种颜色与图案选择，成为活力与时尚的运动必备品。', 'ba8caffe-dd48-4fe2-9cc8-3a9a3abfdd5a', 'LEVEL_3', NULL, NULL, 't', 'f', 160, '女士紧身裤 - 贴合身形的运动时尚', '女士紧身裤系列，采用高弹力、透气吸汗的面料制作。我们的紧身裤贴合身形，展现腿部优美线条，提供良好的支撑性与舒适度，适合瑜伽、健身、跑步等多种运动场合。款式包括高腰设计、全长与七分长度、多种颜色与图案选择，满足不同个人风格与运动需求。每条紧身裤都经过压力测试与穿着实验，确保面料耐用、不透光、不起球。设计注重功能性与时尚感的结合，成为运动与时尚的完美融合，帮助您在运动中保持自信与舒适，展现活力四射的形象。', '女士紧身裤, 高弹力面料, 运动时尚, 舒适支撑', '2025-05-28 03:00:22.510289', '2025-05-28 03:00:22.510289');
INSERT INTO "public"."product_categories" VALUES ('3bddb143-125c-4e04-b0a7-099f456b1472', '哈伦裤', 'HAREM_PANTS_WOMEN', '女士哈伦裤系列，采用宽松裤腿与修身裤腰设计，融合舒适与时尚，展现休闲风格与文化魅力，适合日常穿着与旅行，成为衣橱中的百搭单品。', 'ba8caffe-dd48-4fe2-9cc8-3a9a3abfdd5a', 'LEVEL_3', NULL, NULL, 't', 'f', 170, '女士哈伦裤 - 舒适与时尚的休闲选择', '女士哈伦裤系列，采用宽松裤腿与修身裤腰设计。我们的哈伦裤融合传统与现代元素，展现独特的休闲风格与文化魅力。裤腿宽松部分提供舒适活动空间，而裤腰修身设计确保整体造型不显臃肿。面料选择柔软透气，适合日常穿着、旅行与各种休闲场合。款式包括纯色基本款、民族图案款、刺绣装饰款等多种选择，满足不同搭配需求。哈伦裤能够轻松搭配T恤、衬衫、背心等多种上衣，成为衣橱中的百搭单品，展现随性自在的时尚态度，为您的装扮增添文化深度与个性风格。', '女士哈伦裤, 宽松裤腿, 休闲风格, 文化魅力', '2025-05-28 03:00:22.510289', '2025-05-28 03:00:22.510289');
INSERT INTO "public"."product_categories" VALUES ('eb2f2864-0eaa-408a-9577-2989ad49d147', '阔腿裤', 'WIDE_LEG_PANTS_WOMEN', '女士阔腿裤系列，采用宽大裤腿设计，展现优雅气质与流畅线条，采用舒适面料制作，适合多种场合穿着，成为时尚与舒适的完美结合，彰显女性的自信与魅力。', 'ba8caffe-dd48-4fe2-9cc8-3a9a3abfdd5a', 'LEVEL_3', NULL, NULL, 't', 'f', 180, '女士阔腿裤 - 优雅气质的时尚单品', '女士阔腿裤系列，采用宽大裤腿设计，展现优雅气质与流畅线条。我们的阔腿裤采用柔软垂坠的面料制作，如亚麻、丝绸、棉质等，确保穿着舒适与品质优良。款式包括高腰设计、腰带装饰、纯色与印花等多种选择，适合不同场合穿着，从正式工作环境到休闲聚会。阔腿裤能够修饰身形，遮盖腿部不完美，同时展现女性的自信与魅力。搭配方式多样，可与简约上衣打造优雅造型，或与时尚外套组合呈现前卫风格，成为衣橱中的时尚主角，引领潮流趋势，为您的装扮增添无限可能。', '女士阔腿裤, 宽大裤腿, 优雅气质, 流畅线条', '2025-05-28 03:00:22.511292', '2025-05-28 03:00:22.511292');
INSERT INTO "public"."product_categories" VALUES ('5303b8d1-6c1a-423b-a2c3-d928350e3d11', '女士短裤', 'WOMEN''S_SHORTS_WOMEN', '女士短裤系列，采用柔软面料与修身设计，提供多种款式选择，从休闲到运动风格，为夏季与日常穿着提供理想选择，展现轻松与活力。', 'ba8caffe-dd48-4fe2-9cc8-3a9a3abfdd5a', 'LEVEL_3', NULL, NULL, 't', 'f', 190, '女士短裤 - 轻松活力的夏季选择', '女士短裤系列，采用柔软透气的面料与修身设计制作。我们的短裤款式多样，包括休闲短裤、运动短裤、热裤等多种风格，满足不同需求。面料选择注重吸汗性与舒适度，适合夏季穿着与各种户外活动。设计细节如弹性腰头、侧边抽绳、时尚口袋等，提升实用与美观性。每条短裤都经过精心剪裁与制作，确保穿着舒适、活动自如。无论是搭配T恤、衬衫还是背心，都能展现轻松与活力，成为夏季衣橱中的必备单品，为您的日常生活增添时尚与便利。', '女士短裤, 舒适面料, 修身设计, 夏季穿着', '2025-05-28 03:00:22.51229', '2025-05-28 03:00:22.51229');
INSERT INTO "public"."product_categories" VALUES ('bb138143-13a0-4b6e-ae32-1dbc0a83a576', '唐装', 'TANG_SUIT_WOMEN', '女士唐装系列，融合传统中式元素与现代剪裁，采用精致面料制作，展现东方美学与优雅气质，适合特殊场合与文化活动，成为传统与现代的时尚结合。', 'ba8caffe-dd48-4fe2-9cc8-3a9a3abfdd5a', 'LEVEL_3', NULL, NULL, 't', 'f', 200, '女士唐装 - 传统与现代的优雅融合', '女士唐装系列，融合传统中式元素与现代剪裁设计。我们的唐装采用精致面料如丝绸、提花布、棉麻等制作，展现东方美学的独特魅力。设计细节包括盘扣、立领、云肩、刺绣图案等，展现浓厚的中国文化底蕴。每件唐装都经过精细制作，确保版型合身、质感优良。款式包括唐装外套、连衣裙、旗袍改良款等，适合文化活动、节日庆典、正式场合等穿着。穿着唐装不仅是时尚选择，更是文化传承与审美表达的方式，成为连接传统智慧与现代风格的桥梁，为您的特殊时刻增添优雅与尊贵。', '女士唐装, 传统中式, 东方美学, 文化传承', '2025-05-28 03:00:22.51229', '2025-05-28 03:00:22.51229');
INSERT INTO "public"."product_categories" VALUES ('16f5bd13-3bb4-4eab-8a50-bf68a8b78cf0', '两件套', '2-PIECE_OUTFIT_WOMEN', '女士两件套系列，提供多种搭配组合，如上衣与长裤、外套与连衣裙等，展现协调风格与整体造型，为不同场合提供便捷的穿着选择，节省搭配时间。', 'ba8caffe-dd48-4fe2-9cc8-3a9a3abfdd5a', 'LEVEL_3', NULL, NULL, 't', 'f', 210, '女士两件套 - 协调风格的整体造型', '女士两件套系列，提供多种搭配组合，如上衣与长裤、外套与连衣裙、T恤与短裤等。我们的两件套经过精心设计，确保颜色、图案、面料的协调统一，展现整体造型感。每套服装都注重细节，如统一的领口设计、呼应的装饰元素等，提升整体美感。采用舒适面料制作，确保穿着体验优良。适合不同场合，从日常休闲到正式活动，为忙碌的现代女性节省搭配时间，提供便捷的穿着选择。无论是购买整套还是单独搭配其他单品，都能展现时尚品味与个性风格，成为衣橱中的实用之选。', '女士两件套, 整体造型, 协调风格, 节省搭配', '2025-05-28 03:00:22.513289', '2025-05-28 03:00:22.513289');
INSERT INTO "public"."product_categories" VALUES ('3a70219b-6a08-469c-a405-e02bf1ee2cf2', '连体衣', 'BODYSUIT_WOMEN', '女士连体衣系列，采用修身设计与柔软面料，展现女性曲线，提供多种款式选择，从休闲到时尚风格，为日常穿着与特殊场合提供舒适与优雅的着装选择。', 'ba8caffe-dd48-4fe2-9cc8-3a9a3abfdd5a', 'LEVEL_3', NULL, NULL, 't', 'f', 220, '女士连体衣 - 优雅曲线的时尚选择', '女士连体衣系列，采用修身设计与柔软面料制作。我们的连体衣款式多样，包括紧身连体衣、宽松连体裤、吊带连体衣等多种风格，满足不同需求。面料选择注重弹性与透气性，确保穿着舒适与活动自如。设计细节如V领、蝴蝶结、蕾丝装饰等，展现女性优雅曲线与时尚品味。连体衣适合多种场合，从日常休闲到派对出席，提供优雅的着装选择。每件作品都经过精细剪裁与制作，确保版型完美贴合身形，成为衣橱中的时尚亮点，展现女性的独特魅力与自信风采。', '女士连体衣, 修身设计, 柔软面料, 优雅曲线', '2025-05-28 03:00:22.514303', '2025-05-28 03:00:22.514303');
INSERT INTO "public"."product_categories" VALUES ('8cea7dd7-75e3-47d7-9589-976de815ec24', '运动短裤', 'SPORTS_SHORTS_WOMEN', '女士运动短裤系列，采用高弹力面料与透气设计，提供良好的支撑性与舒适度，适合各种运动与健身活动，展现活力与时尚，成为运动装扮的理想选择。', 'ba8caffe-dd48-4fe2-9cc8-3a9a3abfdd5a', 'LEVEL_3', NULL, NULL, 't', 'f', 230, '女士运动短裤 - 舒适支撑的活力选择', '女士运动短裤系列，采用高弹力、透气吸汗的面料制作。我们的短裤提供良好的支撑性与舒适度，适合跑步、健身、瑜伽等多种运动场合。款式包括紧身运动短裤、宽松运动短裤、带内衬设计等多种选择，满足不同运动需求。设计注重功能性与时尚感的结合，如反光条纹、时尚图案、修身剪裁等，展现活力与时尚。每条短裤都经过运动测试，确保面料耐用、不透光、不变形。无论是专业训练还是日常锻炼，都能提供理想的穿着体验，帮助您在运动中保持专注与自信，成为运动装扮中的必备单品。', '女士运动短裤, 高弹力面料, 透气设计, 舒适支撑', '2025-05-28 03:00:22.514303', '2025-05-28 03:00:22.514303');
INSERT INTO "public"."product_categories" VALUES ('e424c6af-03a1-4572-bd34-31a547c8df13', '藏式服装', 'TIBETAN_CLOTHES_WOMEN', '女士藏式服装系列，采用传统藏族元素与工艺，展现独特的民族风格与文化魅力，成为体验藏族文化与表达个性的理想选择，适合文化活动与特殊场合。', 'ba8caffe-dd48-4fe2-9cc8-3a9a3abfdd5a', 'LEVEL_3', NULL, NULL, 't', 'f', 240, '女士藏式服装 - 民族风格的文化表达', '女士藏式服装系列，采用传统藏族元素与精湛工艺制作。我们的服装展现独特的民族风格与文化魅力，如宽松藏袍、彩色珠饰、传统图案等。面料选择厚实保暖的羊毛、棉布、氆氇等，适合高原气候与各种活动。每件作品都经过手工制作，确保细节精致与品质优良。藏式服装不仅是文化活动与节日庆典的理想选择，更是体验藏族生活方式与表达个性的方式。穿着藏式服装，您将深入参与藏族文化传承，成为文化多样性与民族风情的展现者，为特殊场合带来独特的视觉体验与文化深度。', '藏式服装, 民族风格, 文化传承, 传统工艺', '2025-05-28 03:00:22.51529', '2025-05-28 03:00:22.51529');
INSERT INTO "public"."product_categories" VALUES ('83e5dfdd-1bc1-481f-8dc2-e3d8884730a2', '男士', 'MEN', '男士专属服装系列，包括冥想、瑜伽、日常穿着等多种款式，展现简约与舒适，为现代男性提供全方位的穿着选择，彰显自然气质与个性风格。', '00e865af-c686-404a-8760-dbb3bca5ecbc', 'LEVEL_2', NULL, NULL, 't', 'f', 20, '男士冥想与瑜伽服装', '男士专属服装系列，专为冥想、瑜伽和日常穿着设计。我们的男士服装采用简约剪裁与舒适面料，展现自然气质与个性风格。款式多样，从宽松的冥想长裤到修身的瑜伽T恤，从休闲外套到传统唐装，满足不同场合需求。每件作品都融合传统元素与现代设计，确保穿着舒适与活动自如，帮助现代男性在繁忙生活中保持内心平静与外在整齐。无论是寻找冥想服饰、瑜伽装备还是日常休闲装，我们的服装系列都能满足您的需求，成为您身心实践和时尚表达的理想选择。', '男士冥想服装, 瑜伽T恤, 休闲外套, 传统唐装', '2025-05-28 03:00:22.51629', '2025-05-28 03:00:22.51629');
INSERT INTO "public"."product_categories" VALUES ('3524304d-c372-4449-8743-562a47903692', '冥想瑜伽服', 'MEDITATION_QIGONG_CLOTHES_MEN', '专为男士设计的冥想瑜伽服装，采用宽松剪裁与柔软面料，确保舒适与自由移动，帮助深度放松与专注练习，展现简约的修行姿态。', '83e5dfdd-1bc1-481f-8dc2-e3d8884730a2', 'LEVEL_3', NULL, NULL, 't', 'f', 200, '男士冥想瑜伽服 - 舒适与简约的修行选择', '专为男士设计的冥想瑜伽服装系列，采用宽松剪裁与柔软面料制作。我们的服装确保舒适与自由移动，帮助您在练习中深度放松与专注。面料采用有机棉、竹纤维等天然材料，透气吸汗，适合各种瑜伽、冥想、气功练习。款式包括宽松长裤、舒适上衣、套装等多种选择，展现简约的修行姿态。每件作品都经过精心设计，细节考究，为您的练习带来全方位的舒适体验，成为您精神实践的理想着装。', '男士瑜伽服, 冥想服装, 宽松长裤, 舒适上衣', '2025-05-28 03:00:22.51629', '2025-05-28 03:00:22.51629');
INSERT INTO "public"."product_categories" VALUES ('365a40d4-a193-4a42-b756-1bd97d6ce679', '佛系T恤', 'BUDDHA_INSPIRED_T-SHIRT_MEN', '男士佛系主题T恤，融合佛教元素与现代设计，采用优质棉料制作，展现精神内涵与时尚风格，成为日常穿着的理想选择，传递平和与智慧。', '83e5dfdd-1bc1-481f-8dc2-e3d8884730a2', 'LEVEL_3', NULL, NULL, 't', 'f', 210, '男士佛系T恤 - 精神内涵的时尚表达', '男士佛系主题T恤系列，融合佛教元素与现代设计。我们的T恤采用优质棉料制作，亲肤透气，版型修身。图案设计包括佛像、经文、莲花等多种宗教符号，展现精神内涵与艺术美感。这些T恤不仅是日常穿着的理想选择，更是表达个人信仰与追求平和的理想方式。每件作品都经过精心印刷，确保色彩鲜艳持久，图案细节清晰。适合各种场合穿着，为您的日常装扮增添文化深度与时尚风格，成为连接内心与外在的桥梁。', '佛系T恤, 佛教元素, 精神内涵, 日常穿着', '2025-05-28 03:00:22.51629', '2025-05-28 03:00:22.51629');
INSERT INTO "public"."product_categories" VALUES ('f61fdd9d-346b-4bf2-8680-ea4eeee167db', '上衣', 'SHIRT_MEN', '男士上衣系列，采用舒适面料与经典剪裁，展现简约与大气，适合多种场合穿着，成为衣橱中的百搭单品，彰显自然气质与个性风格。', '83e5dfdd-1bc1-481f-8dc2-e3d8884730a2', 'LEVEL_3', NULL, NULL, 't', 'f', 220, '男士上衣 - 舒适与经典的日常选择', '男士上衣系列，采用舒适面料与经典剪裁制作。我们的上衣款式多样，包括宽松T恤、修身衬衫、柔软针织衫等，展现简约与大气。面料选择注重透气性与耐用性，适合日常穿着、冥想练习或休闲出行。每款上衣都经过精心设计，细节处理考究，能够轻松搭配各种下装，成为衣橱中的百搭单品。无论是追求休闲风格还是优雅气质，都能找到适合的选择，彰显自然气质与个性魅力。', '男士上衣, 舒适面料, 经典剪裁, 百搭配饰', '2025-05-28 03:00:22.517806', '2025-05-28 03:00:22.517806');
INSERT INTO "public"."product_categories" VALUES ('4a9e3456-33a2-4615-9b7e-fa6301c6cf17', '长裤', 'PANTS_MEN', '男士长裤系列，采用舒适面料与修身剪裁，提供多种款式如直筒裤、宽松裤、瑜伽裤等，满足不同风格需求，为日常穿着与冥想练习提供理想选择，展现自然舒适与时尚风格。', '83e5dfdd-1bc1-481f-8dc2-e3d8884730a2', 'LEVEL_3', NULL, NULL, 't', 'f', 230, '男士长裤 - 舒适与风格的完美结合', '男士长裤系列，采用柔软舒适的面料与修身剪裁制作。我们的长裤款式丰富，包括直筒裤、宽松裤、瑜伽裤、工装裤等，满足不同风格与需求。面料选择注重透气性与弹性，确保穿着舒适，适合日常穿着、冥想练习与各种活动。设计细节如多口袋、抽绳腰头、强化膝部等，提升实用与造型感。每条长裤都经过精细制作，确保版型稳定与品质优良。无论是追求休闲风格、运动装扮还是优雅气质，都能找到理想的款式，成为衣橱中的实用单品，展现自然舒适与时尚风格的完美结合。', '男士长裤, 舒适面料, 修身剪裁, 风格多样', '2025-05-28 03:00:22.518817', '2025-05-28 03:00:22.518817');
INSERT INTO "public"."product_categories" VALUES ('d4dbad47-4e7f-448e-be7b-ec461a4f2f5d', '外套', 'COATS_JACKETS_MEN', '男士外套系列，采用保暖面料与时尚设计，提供多种款式选择，从休闲夹克到优雅大衣，为不同季节与场合提供理想搭配，展现男性的稳重与时尚态度。', '83e5dfdd-1bc1-481f-8dc2-e3d8884730a2', 'LEVEL_3', NULL, NULL, 't', 'f', 240, '男士外套 - 保暖与时尚的完美融合', '男士外套系列，采用高品质保暖面料与时尚设计制作。我们的外套款式多样，包括休闲夹克、连帽外套、修身大衣、皮草外套等，适合不同季节与场合穿着。设计注重细节，如精致刺绣、独特领口、功能性口袋等，展现男性的稳重与时尚态度。外套不仅提供出色的保暖性能，更通过精心剪裁与时尚元素提升整体造型。无论是日常通勤、冥想旅行还是社交活动，都能找到理想的搭配，成为您衣橱中的必备单品，为您的装扮增添层次感与风格亮点。', '男士外套, 保暖夹克, 优雅大衣, 时尚设计', '2025-05-28 03:00:22.519818', '2025-05-28 03:00:22.519818');
INSERT INTO "public"."product_categories" VALUES ('39cad863-d669-4cad-9d48-ef281329d233', '按活动分类', 'SHOP_BY_ACTIVITY', '根据不同活动场景设计的服装系列，包括瑜伽、冥想、太极等，确保每种活动都能找到合适的穿着选择，展现功能性与文化深度，支持身心实践的全方位需求。', '00e865af-c686-404a-8760-dbb3bca5ecbc', 'LEVEL_2', NULL, NULL, 't', 'f', 30, '活动专属服装 - 功能性与文化的完美结合', '根据不同活动场景设计的服装系列，包括瑜伽、冥想、太极等。我们的活动专属服装采用功能性面料与专业剪裁，确保每种活动都能找到合适的穿着选择。瑜伽服装提供高弹力与透气性，冥想服装注重宽松舒适与宁静氛围，太极服装则结合传统元素与流畅动作需求。每件作品都融合文化深度与现代设计，支持身心实践的全方位需求。无论您是专业练习者还是初学者，都能在我们的系列中找到理想的服装，帮助提升练习效果，展现文化内涵与个人风格。', '活动服装, 瑜伽服装, 冥想服饰, 太极服装', '2025-05-28 03:00:22.520819', '2025-05-28 03:00:22.520819');
INSERT INTO "public"."product_categories" VALUES ('1fbe1c95-d916-4676-9514-e8e95ca7dd78', '瑜伽', 'YOGA', '专为瑜伽练习设计的服装系列，采用高弹力面料与修身剪裁，确保舒适与自由移动，帮助深度拉伸与平衡练习，展现优雅的练习姿态。', '39cad863-d669-4cad-9d48-ef281329d233', 'LEVEL_3', NULL, NULL, 't', 'f', 300, '瑜伽服装 - 舒适与功能性的完美结合', '专为瑜伽练习设计的服装系列，采用高弹力、透气吸汗的面料与修身剪裁制作。我们的瑜伽服装确保舒适与自由移动，帮助您在练习中深度拉伸与保持平衡。款式包括紧身裤、运动背心、瑜伽外套等多种选择，满足不同瑜伽风格与环境需求。设计注重细节，如无缝拼接、加长腰头、抗菌处理等，提升穿着体验。每件作品都经过瑜伽大师测试，确保符合人体工学与瑜伽动作需求。无论是参加热瑜伽、哈他瑜伽、流动瑜伽还是冥想课程，都能找到理想的服装，成为您练习中的得力助手，展现优雅的练习姿态与专业精神。', '瑜伽服装, 高弹力面料, 修身剪裁, 舒适移动', '2025-05-28 03:00:22.520819', '2025-05-28 03:00:22.520819');
INSERT INTO "public"."product_categories" VALUES ('0afd7191-46da-42c5-ab2e-33757a7dec37', '冥想', 'MEDITATION_ACTIVITY', '专为冥想练习设计的服装系列，采用宽松剪裁与柔软面料，创造宁静氛围，帮助放松身心，进入深度冥想状态，展现平和的修行姿态。', '39cad863-d669-4cad-9d48-ef281329d233', 'LEVEL_3', NULL, NULL, 't', 'f', 310, '冥想服装 - 宁静与舒适的修行选择', '专为冥想练习设计的服装系列，采用宽松剪裁与柔软面料制作。我们的冥想服装创造宁静氛围，帮助您放松身心，进入深度冥想状态。面料选择注重透气性与轻盈感，如有机棉、亚麻、丝绸等，确保长时间穿着的舒适度。款式包括宽松长裤、舒适上衣、长袍等多种选择，适合不同冥想姿势与环境。设计细节如宽松袖口、低领设计、纯色系等，减少视觉与身体干扰。每件作品都经过声学测试，确保面料摩擦声最小化，帮助维持冥想环境的安静。穿着冥想服装不仅是功能选择，更是心灵修行的外在表达，为您的精神实践增添和谐与专注。', '冥想服装, 宽松剪裁, 软软面料, 宁静氛围', '2025-05-28 03:00:22.521816', '2025-05-28 03:00:22.521816');
INSERT INTO "public"."product_categories" VALUES ('a73ff6e6-cab0-4829-85b5-5e98c11ce7ae', '太极/气功', 'TAICHI_QIGONG', '专为太极与气功练习设计的服装系列，融合传统元素与现代面料，确保流畅动作与舒适穿着，展现东方美学与优雅气质，支持传统身心练习的完美表达。', '39cad863-d669-4cad-9d48-ef281329d233', 'LEVEL_3', NULL, NULL, 't', 'f', 320, '太极/气功服装 - 传统与现代的完美融合', '专为太极与气功练习设计的服装系列，融合传统元素与现代面料制作。我们的服装确保流畅动作与舒适穿着，采用柔软、轻盈、具有一定弹性的面料，如棉混纺、功能性丝绸等，适合缓慢而精准的动作需求。款式包括传统太极服、改良长袍、宽松裤装等多种选择，展现东方美学与优雅气质。设计细节如盘扣、立领、云肩等传统元素，与现代剪裁相结合，既尊重传统文化又符合当代审美。每件作品都经过太极大师与气功教练的测试，确保符合练习中的动作幅度与呼吸需求。穿着太极/气功服装，您将深入体验传统身心练习的精神内涵，展现优雅的练习姿态与文化传承。', '太极服装, 气功服饰, 传统元素, 东方美学', '2025-05-28 03:00:22.521816', '2025-05-28 03:00:22.521816');
INSERT INTO "public"."product_categories" VALUES ('4841d455-7b84-47ed-a3d2-93d5e42d407c', '配饰', 'ACCESSORIES', '丰富多样的配饰系列，包括包包、围巾、毛毯等，采用优质材料与精致工艺，展现实用功能与时尚美感，为整体造型增添亮点与温暖感受。', '00e865af-c686-404a-8760-dbb3bca5ecbc', 'LEVEL_2', NULL, NULL, 't', 'f', 40, '时尚配饰 - 实用与美学的完美结合', '丰富多样的配饰系列，包括包包、围巾、毛毯等。我们的配饰采用优质材料与精致工艺制作，展现实用功能与时尚美感。包包系列包括手提包、斜挎包、冥想包等多种类型，适合不同场合与需求。围巾采用柔软面料如羊绒、蚕丝、有机棉等制作，提供保暖与装饰双重功能。毛毯系列采用厚实面料，适合冥想垫、瑜伽铺巾、家居装饰等多种用途。每件配饰都经过精心设计，确保品质优良与细节完美，为您的整体造型增添亮点，带来温暖与舒适的使用体验。无论是作为礼物还是自用，这些配饰都能成为日常生活的实用伙伴与时尚声明。', '时尚配饰, 实用功能, 精致工艺, 保暖装饰', '2025-05-28 03:00:22.522817', '2025-05-28 03:00:22.522817');
INSERT INTO "public"."product_categories" VALUES ('70b7b4d8-8e9d-4c56-85dd-772c06b2fe42', '包包', 'BAGS', '时尚包包系列，采用优质材料制作，设计多样，从简约手提包到多功能背包，满足不同场合与需求，展现个性风格与实用功能，成为出行的理想伴侣。', '4841d455-7b84-47ed-a3d2-93d5e42d407c', 'LEVEL_3', NULL, NULL, 't', 'f', 400, '时尚包包 - 个性风格的实用选择', '时尚包包系列，采用优质材料如皮革、帆布、再生纤维等制作。我们的包包设计多样，包括手提包、斜挎包、背包、冥想包等多种类型，满足不同场合与需求。注重功能性细节，如宽敞内部空间、多功能隔层、防水涂层、加固背带等，确保实用与耐用。设计风格从简约现代到民族传统，展现个性风格与文化深度。每个包包都经过严格质量检验，确保拉链顺畅、面料坚固、外观精致。无论是日常通勤、旅行探险还是冥想修行，都能找到理想的包包，成为您出行的得力助手，展现独特品味与生活态度。', '时尚包包, 优质材料, 功能设计, 个性风格', '2025-05-28 03:00:22.523816', '2025-05-28 03:00:22.523816');
INSERT INTO "public"."product_categories" VALUES ('d17378c1-5046-4360-99ee-75182a26e5ec', '围巾+披肩', 'SCARVES+SHAWLS', '柔软围巾与披肩系列，采用高级面料如羊绒、蚕丝、 modal 等制作，提供温暖与优雅的佩戴体验，成为季节转换与风格搭配的理想选择，展现女性的柔美与气质。', '4841d455-7b84-47ed-a3d2-93d5e42d407c', 'LEVEL_3', NULL, NULL, 't', 'f', 410, '柔软围巾与披肩 - 温暖与优雅的时尚单品', '柔软围巾与披肩系列，采用高级面料如羊绒、蚕丝、 modal、有机棉等制作。我们的围巾与披肩提供温暖与优雅的佩戴体验，适合季节转换与各种风格搭配。款式多样，包括窄围巾、大方巾、长披肩、短斗篷等多种选择，满足不同场合需求。设计注重色彩搭配与图案设计，从纯色经典到民族印花、几何图案等，展现女性的柔美与气质。围巾与披肩不仅具有保暖功能，更是整体造型的点睛之笔，能够瞬间提升穿搭的层次感与时尚度。每件作品都经过精细制作，确保面料柔软、色泽鲜艳、边缘整齐，成为衣橱中的百搭单品，为您的装扮增添无限魅力。', '柔软围巾, 高级面料, 优雅披肩, 温暖搭配', '2025-05-28 03:00:22.523816', '2025-05-28 03:00:22.523816');
INSERT INTO "public"."product_categories" VALUES ('09c86466-821a-44b2-9210-36a618d08a78', '毛毯', 'BLANKET', '舒适毛毯系列，采用厚实面料如羊毛、棉布、亚麻等制作，适合冥想垫、瑜伽铺巾、家居装饰等多种用途，为身心实践与日常休息提供温暖与舒适的支持。', '4841d455-7b84-47ed-a3d2-93d5e42d407c', 'LEVEL_3', NULL, NULL, 't', 'f', 420, '舒适毛毯 - 温暖与实用的家居选择', '舒适毛毯系列，采用厚实保暖的面料如羊毛、棉布、亚麻等制作。我们的毛毯适合多种用途，包括冥想垫、瑜伽铺巾、沙发毯、床毯等，为您的身心实践与日常休息提供温暖与舒适的体验。面料经过特殊处理，确保柔软度、透气性与耐用性，部分款式还具有抗菌、防螨等健康功能。设计风格多样，从简约纯色到民族图案、几何纹理等，适合不同家居装饰风格。每条毛毯都经过精细织造与质量检验，确保尺寸稳定、色彩牢固、触感优良。无论是作为冥想辅助工具、瑜伽练习铺巾还是家居装饰品，毛毯都能为您带来全方位的舒适感受，成为生活中的温暖伴侣。', '舒适毛毯, 厚实面料, 冥想垫毯, 家居装饰', '2025-05-28 03:00:22.524815', '2025-05-28 03:00:22.524815');
INSERT INTO "public"."product_categories" VALUES ('0fb693d4-66d7-4633-9d09-1473c3038f6e', '佛像', 'STATUES', '精美的佛像系列，包括释迦牟尼佛、笑佛、观音菩萨、象神等多种造型，采用优质材料制作，展现庄严与慈悲，为您的修行与家居带来神圣氛围。', '1bc893b2-5227-4cd2-871d-10cdf3b89da4', 'LEVEL_2', NULL, NULL, 't', 'f', 10, '佛像系列 - 庄严慈悲的精神象征', '精美的佛像系列，包括释迦牟尼佛、笑佛、观音菩萨、象神等多种造型。我们的佛像采用黄铜、黑檀、水晶、树脂等优质材料制作，每尊佛像都经过细致雕刻与精细打磨，展现庄严与慈悲的神态。佛像不仅作为冥想修行的焦点，帮助集中注意力与净化心灵，更是家居装饰中的神圣元素，为您的空间带来宁静与祥和。每尊佛像都附有详细的背景介绍与摆放建议，帮助您深入了解其文化意义与精神价值，成为您修行道路上的重要伴侣。', '佛像系列, 庄严佛像, 慈悲神态, 修行焦点', '2025-05-28 03:00:22.525824', '2025-05-28 03:00:22.525824');
INSERT INTO "public"."product_categories" VALUES ('05e3d800-057d-497a-8916-e406dae5cfea', '释迦牟尼佛像', 'BUDDHA STATUE', '释迦牟尼佛像系列，展现佛陀的庄严与智慧，采用传统工艺制作，适合冥想修行与家居供奉，成为精神觉悟的象征与文化传承的载体。', '0fb693d4-66d7-4633-9d09-1473c3038f6e', 'LEVEL_3', NULL, NULL, 't', 'f', 100, '释迦牟尼佛像 - 庄严智慧的觉悟象征', '释迦牟尼佛像系列，展现佛陀的庄严与智慧。我们的佛像采用传统工艺制作，遵循佛教经典的比例与特征，确保每尊佛像都符合宗教规范。材质包括黄铜、黑檀、水晶等多种选择，每尊佛像都经过精细打磨与开光加持，增强其灵性能量。释迦牟尼佛像适合冥想修行时作为观想对象，帮助修行者集中注意力、净化心灵、提升觉悟。同时，佛像也是家居供奉的理想选择，为您的空间带来神圣氛围与文化深度。每尊佛像都附有详细的经文解释与修行指导，帮助您深入理解佛教教义，走在觉悟之路上。', '释迦牟尼佛像, 庄严智慧, 冥想修行, 家居供奉', '2025-05-28 03:00:22.526822', '2025-05-28 03:00:22.526822');
INSERT INTO "public"."product_categories" VALUES ('07ae0908-da25-43cf-b1f1-82c3123b1ebe', '笑佛像', 'LAUGHING BUDDHA STATUES', '笑佛像系列，展现弥勒佛的欢乐与富足寓意，采用圆润造型与温暖材质制作，为您的空间带来喜乐能量，成为吸引好运与繁荣的理想摆件。', '0fb693d4-66d7-4633-9d09-1473c3038f6e', 'LEVEL_3', NULL, NULL, 't', 'f', 110, '笑佛像 - 欢乐富足的喜乐象征', '笑佛像系列，展现弥勒佛的欢乐与富足寓意。我们的笑佛像采用圆润造型与温暖材质如黄铜、陶瓷、树脂等制作，展现弥勒佛大肚能容、笑口常开的亲切形象。每尊笑佛都经过精细雕刻，确保表情生动、细节丰富，传递喜乐能量与积极心态。笑佛像适合放置在客厅、办公室、店铺等空间，作为吸引好运与繁荣的理想摆件。在佛教传统中，弥勒佛象征着未来觉悟与世间欢乐，我们的笑佛像将这种精神内涵具象化，为您的生活空间带来正能量与美好祝福。', '笑佛像, 弥勒佛像, 欢乐寓意, 富足象征', '2025-05-28 03:00:22.526822', '2025-05-28 03:00:22.526822');
INSERT INTO "public"."product_categories" VALUES ('8822a91d-d5e3-415e-b245-3725b3598b79', '观音菩萨像', 'KWAN YIN STATUES', '观音菩萨像系列，展现慈悲与救度的神圣形象，采用优雅造型与细腻工艺制作，为您的修行与家居带来安宁与庇护，成为心灵慰藉的源泉。', '0fb693d4-66d7-4633-9d09-1473c3038f6e', 'LEVEL_3', NULL, NULL, 't', 'f', 120, '观音菩萨像 - 慈悲救度的神圣象征', '观音菩萨像系列，展现慈悲与救度的神圣形象。我们的观音像采用优雅造型与细腻工艺制作，材质包括玉石、黑檀、琉璃、青铜等多种选择，每尊菩萨像都经过精心雕刻与打磨，展现柔和面容与慈悲眼神。观音菩萨在佛教中被视为慈悲的化身，能够救苦救难、回应众生祈求。我们的观音像不仅适合冥想修行时作为观想对象，帮助培养慈悲心与智慧，更是家居供奉的理想选择，为您的空间带来安宁与庇护。每尊观音像都附有详细的经文介绍与摆放建议，帮助您深入了解其精神内涵与文化价值，成为心灵慰藉与精神支持的重要象征。', '观音菩萨像, 慈悲救度, 宁静庇护, 精美雕刻', '2025-05-28 03:00:22.527817', '2025-05-28 03:00:22.527817');
INSERT INTO "public"."product_categories" VALUES ('be178bf7-c03b-48d8-9602-05b906ea6cba', '象神像', 'GANESH STATUES', '象神像系列，展现象头神甘尼许的智慧与力量，采用传统造型与优质材料制作，帮助去除障碍，为您的生活与修行带来好运与成功。', '0fb693d4-66d7-4633-9d09-1473c3038f6e', 'LEVEL_3', NULL, NULL, 't', 'f', 130, '象神像 - 智慧力量的障碍消除者', '象神像系列，展现象头神甘尼许的智慧与力量。我们的象神像采用传统造型与优质材料如黄铜、黑檀、树脂等制作，每尊像都经过精细雕刻，展现甘尼许的特征：象头人身、大肚、多臂，手持各种法器。在印度教传统中，甘尼许被视为智慧之神、成功之神，能够消除障碍、带来好运。我们的象神像适合放置在入口处、书桌、冥想空间等位置，作为去除障碍、开启成功之路的神圣象征。每尊象神像都附有详细的神话背景与祈福方法，帮助您连接古老的智慧传统，为生活与修行带来积极能量与保护力量。', '象神像, 甘尼许, 智慧力量, 障碍消除', '2025-05-28 03:00:22.527817', '2025-05-28 03:00:22.527817');
INSERT INTO "public"."product_categories" VALUES ('648bd9e4-f161-4b86-9aaa-46a9486d5acf', '冥想瑜伽佛像', 'MEDITATION YOGA STATUE', '冥想瑜伽佛像系列，展现佛菩萨的冥想姿态与瑜伽精神，采用稳定造型与和谐比例制作，为您的练习空间带来专注能量，成为修行的理想陪伴。', '0fb693d4-66d7-4633-9d09-1473c3038f6e', 'LEVEL_3', NULL, NULL, 't', 'f', 140, '冥想瑜伽佛像 - 专注能量的修行伴侣', '冥想瑜伽佛像系列，展现佛菩萨的冥想姿态与瑜伽精神。我们的佛像采用稳定造型与和谐比例制作，材质包括黄铜、黑檀、陶瓷等多种选择，每尊像都经过精细雕刻，展现平和坐姿与专注神态。这些佛像专为冥想与瑜伽练习空间设计，能够帮助创造宁静氛围，增强修行能量。佛像的稳定造型象征内心的平静与专注，适合放置在冥想角落、瑜伽垫旁或安静的书房中。每尊佛像都附有详细的修行指导与空间布置建议，帮助您打造理想的练习环境，成为您每日修行与自我探索的忠实伴侣，引导您走向内心的平衡与觉醒之路。', '冥想瑜伽佛像, 专注能量, 修行陪伴, 稳定造型', '2025-05-28 03:00:22.529138', '2025-05-28 03:00:22.529138');
INSERT INTO "public"."product_categories" VALUES ('ae6c4361-2f5f-4133-80bb-a7c1fcb70588', '家宅饰品目录', 'CATEGORIES_HOME_DECOR', '家居装饰与个人用品的精选分类，包括香薰炉、钥匙链、装饰品、禅意花园等多种实用与美观兼具的商品，为您的生活空间增添和谐与个性。', '1bc893b2-5227-4cd2-871d-10cdf3b89da4', 'LEVEL_2', NULL, NULL, 't', 'f', 20, '家居装饰品类 - 和谐美观的生活选择', '家居装饰与个人用品的精选分类，包括香薰炉、钥匙链、装饰品、禅意花园等多种实用与美观兼具的商品。我们的产品经过精心挑选，融合传统工艺与现代设计，展现独特风格与卓越品质。香薰炉帮助净化空气、创造冥想氛围，钥匙链与车挂增添日常便利与个性表达，装饰品提升空间美感，禅意花园提供微型冥想焦点。每件商品都注重细节，确保使用体验优良，为您的生活空间增添和谐与个性，成为连接物质舒适与精神宁静的桥梁。', '家居装饰, 香薰炉, 装饰品, 禅意花园', '2025-05-28 03:00:22.530137', '2025-05-28 03:00:22.530137');
INSERT INTO "public"."product_categories" VALUES ('ef5e5203-97df-468d-bfa0-2a3d64f4c1ca', '香薰炉与香料', 'INCENSE BURNERS & INCENSE', '香薰炉与香料系列，采用优质材料制作香薰炉，搭配天然香料，帮助净化空间、提升意识，创造理想的冥想与生活氛围，展现嗅觉疗愈的力量。', 'ae6c4361-2f5f-4133-80bb-a7c1fcb70588', 'LEVEL_3', NULL, NULL, 't', 'f', 200, '香薰炉与香料 - 净化空间的嗅觉疗愈', '香薰炉与香料系列，采用优质陶瓷、金属、石材等材料制作香薰炉，搭配天然植物香料。我们的香薰炉设计精美，实用耐用，香料种类丰富，包括沉香、檀香、藏香等多种传统配方。燃烧香料产生的烟雾与香气能够净化空间、提升意识、缓解压力、促进放松，是冥想、瑜伽、阅读等安静活动的理想伴侣。在许多文化中，香薰被视为连接物质世界与精神世界的桥梁，我们的产品将这种古老智慧带入现代生活，帮助您创造和谐宁静的氛围，提升日常生活品质。每套香薰产品都附有使用指南与香料搭配建议，确保您获得最佳的嗅觉疗愈体验。', '香薰炉, 天然香料, 空间净化, 嗅觉疗愈', '2025-05-28 03:00:22.531144', '2025-05-28 03:00:22.531144');
INSERT INTO "public"."product_categories" VALUES ('c939f87d-6cd9-405a-9e7f-8b74ae1e2797', '钥匙链 + 车挂', 'KEYCHAIN + CAR HANGING', '钥匙链与车挂系列，融合实用功能与个性设计，采用优质材料制作，展现时尚风格与文化元素，为日常出行增添便利与精神守护。', 'ae6c4361-2f5f-4133-80bb-a7c1fcb70588', 'LEVEL_3', NULL, NULL, 't', 'f', 210, '钥匙链与车挂 - 实用与个性的随身伴侣', '钥匙链与车挂系列，融合实用功能与个性设计。我们的产品采用金属、皮革、宝石、佛像等多种材料制作，确保耐用性与美观度。设计风格多样，从简约现代到宗教文化，满足不同个性需求。钥匙链帮助整理钥匙，防止丢失，车挂则为您的爱车增添个性装饰与精神守护。许多款式融入佛教、印度教等文化元素，如佛像、六字真言、吉祥图案等，寓意平安、智慧、好运。这些小物件不仅是日常用品，更成为精神信念的随身表达，为您的出行带来便利与正能量，成为生活中的贴心伴侣与文化使者。', '钥匙链, 车挂饰品, 个性设计, 精神守护', '2025-05-28 03:00:22.531144', '2025-05-28 03:00:22.531144');
INSERT INTO "public"."product_categories" VALUES ('7604d919-b3dc-491f-bf9c-89d6657e7cd1', '装饰品', 'DECOR', '家居装饰品系列，包括摆件、挂饰、储物用品等，采用多样材质与设计风格，为您的生活空间增添美感与个性，创造和谐舒适的居住环境。', 'ae6c4361-2f5f-4133-80bb-a7c1fcb70588', 'LEVEL_3', NULL, NULL, 't', 'f', 220, '家居装饰品 - 美学与实用的完美结合', '家居装饰品系列，包括摆件、挂饰、储物用品等多种类型。我们的产品采用陶瓷、木材、金属、玻璃等多种材质制作，设计风格从现代简约到民族传统，满足不同家居装饰需求。装饰品不仅提升空间美感，更注重实用功能，如带储物空间的摆件、可调节的挂饰、兼具装饰与使用的托盘等。每件作品都经过精心设计与制作，确保品质优良与细节完美。摆放合适的装饰品能够反映居住者的个性与品味，为家居环境增添和谐能量，创造舒适宜人的生活氛围。我们的装饰品系列帮助您打造独特风格的居住空间，成为美学与实用的完美结合。', '家居装饰品, 摆件挂饰, 实用功能, 美学风格', '2025-05-28 03:00:22.532136', '2025-05-28 03:00:22.532136');
INSERT INTO "public"."product_categories" VALUES ('5894bde9-4f8b-48d7-871f-94e3d4e9641b', '冥想禅园', 'MEDITATION ZEN GARDENS', '微型禅意花园系列，通过砂石、小雕塑、植物等元素创造冥想焦点，培养专注与耐心，展现日本禅宗美学，为室内空间增添宁静与冥想氛围。', 'ae6c4361-2f5f-4133-80bb-a7c1fcb70588', 'LEVEL_3', NULL, NULL, 't', 'f', 230, '冥想禅园 - 日本禅宗美学的室内冥想工具', '微型禅意花园系列，通过砂石、小雕塑、植物等元素创造冥想焦点。我们的禅园设计精美，采用优质材料如陶瓷盆、天然砂石、小型佛像、植物盆栽等制作，展现日本禅宗美学的核心要素。禅园通过简约的设计与自然元素的结合，帮助培养专注力与耐心，成为理想的冥想辅助工具。使用禅园时，您可以通过耙砂、摆放小景等互动方式，进入深度放松状态，体验禅修的宁静与智慧。这些禅园适合放置在书桌、窗台、边几等位置，为室内空间增添宁静氛围，成为日常冥想与精神修养的重要部分，连接自然与内心平静，展现东方美学的独特魅力。', '禅意花园, 禅宗美学, 冥想焦点, 日本文化', '2025-05-28 03:00:22.532136', '2025-05-28 03:00:22.532136');
INSERT INTO "public"."product_categories" VALUES ('a02c92e7-45c0-4543-abbb-3d20ca466f41', '可爱动物装饰', 'CUTE ANIMAL DECOR', '可爱动物造型装饰品系列，以树脂、陶瓷等材质制作，展现动物的灵动与趣味，为家居增添活泼氛围，成为表达个性与爱心的理想装饰选择。', 'ae6c4361-2f5f-4133-80bb-a7c1fcb70588', 'LEVEL_3', NULL, NULL, 't', 'f', 240, '可爱动物装饰 - 活泼趣味的个性表达', '可爱动物造型装饰品系列，以树脂、陶瓷、毛绒等多种材质制作。我们的产品展现动物的灵动与趣味，如猫咪、狗狗、兔子、狐狸等形象栩栩如生，表情丰富。设计风格从写实到卡通，满足不同审美需求。这些装饰品适合放置在客厅、卧室、儿童房、办公室等空间，为环境增添活泼氛围与温馨感受。可爱动物装饰不仅是家居摆件，更是情感表达的方式，能够唤起人们对自然与生命的热爱。每件作品都经过精心制作，确保安全无毒、手感优良，成为表达个性与爱心的理想选择，特别适合赠送动物爱好者与儿童，为生活带来欢乐与温暖。', '动物装饰, 可爱造型, 活泼氛围, 个性表达', '2025-05-28 03:00:22.533138', '2025-05-28 03:00:22.533138');
INSERT INTO "public"."product_categories" VALUES ('df2e0873-6539-47e8-9c4d-61c342204336', '八卦图', 'BAGUA MAP', '风水八卦图系列，采用传统符号与色彩设计，帮助能量流动与空间布局，为家居与工作环境带来和谐与平衡，展现风水文化的应用智慧。', 'ae6c4361-2f5f-4133-80bb-a7c1fcb70588', 'LEVEL_3', NULL, NULL, 't', 'f', 250, '风水八卦图 - 能量流动的空间指南', '风水八卦图系列，采用传统符号与色彩设计制作。我们的八卦图以优质丝绸、纸张、亚克力等材料呈现，展现完整的八卦符号与九宫格布局，部分产品还融入生肖、星宿等元素，增强风水应用效果。八卦图在风水实践中用于分析能量流动、指导空间布局，帮助平衡气场、提升运势。我们的八卦图提供多种尺寸与风格选择，适合挂在客厅、办公室、玄关等重要位置。每张八卦图都附有详细的使用指南与风水原理解释，帮助您正确应用这一古老智慧，为家居与工作环境带来和谐与平衡，成为连接传统文化与现代生活的实用工具。', '风水八卦图, 能量流动, 空间布局, 风水文化', '2025-05-28 03:00:22.534136', '2025-05-28 03:00:22.534136');
INSERT INTO "public"."product_categories" VALUES ('34dde886-3bee-402f-8f99-652d14634800', '茶杯', 'TEA CUP', '精美茶杯系列，采用优质陶瓷、紫砂等材质制作，展现传统工艺与文化内涵，为品茶时刻带来愉悦体验，成为茶道与日常饮用的理想器具。', 'ae6c4361-2f5f-4133-80bb-a7c1fcb70588', 'LEVEL_3', NULL, NULL, 't', 'f', 260, '精美茶杯 - 传统工艺的品茶享受', '精美茶杯系列，采用优质陶瓷、紫砂、玻璃等材质制作。我们的茶杯展现传统工艺的精湛技艺，从手工拉坯、雕刻到釉彩绘制，每一步都经过严格把关。设计风格包括简约现代、古典青花、日式和风、中式典雅等多种选择，满足不同文化背景与审美需求。茶杯不仅注重外观美感，更强调实用功能，如良好的握持感、适度的容量、优质的材质确保茶香纯正。品茶时使用精美茶杯，不仅提升饮用体验，更成为文化交流与精神享受的重要部分。我们的茶杯适合茶道爱好者、收藏家以及追求生活品质的人士，为您的品茶时刻增添传统韵味与现代美感。', '精美茶杯, 传统工艺, 品茶体验, 茶道器具', '2025-05-28 03:00:22.534136', '2025-05-28 03:00:22.534136');
INSERT INTO "public"."product_categories" VALUES ('7c38698d-7db3-48e5-882f-76aee3bfd999', '扇子', 'FAN', '传统扇子系列，采用丝绸、纸张、竹木等材质制作，展现东方工艺与文化美学，为夏日带来清凉，成为文化传承与时尚装饰的理想结合。', 'ae6c4361-2f5f-4133-80bb-a7c1fcb70588', 'LEVEL_3', NULL, NULL, 't', 'f', 270, '传统扇子 - 东方美学的清凉伴侣', '传统扇子系列，采用丝绸、纸张、竹木等优质材质制作。我们的扇子展现东方工艺的精湛技艺，包括手工绘画、刺绣、雕刻等多种装饰技法，呈现山水、花鸟、人物、吉祥图案等丰富题材。扇子类型涵盖折扇、团扇、羽扇等多种形式，适合不同场合与个人风格。在实用性方面，扇子为夏日带来自然清凉，同时作为一种文化符号，体现了东方智慧与审美情趣。我们的扇子不仅适合自用，更是赠送亲友、文化交流的理想礼物，帮助传承传统工艺，展现文化自信。每把扇子都经过精心包装与保养说明，确保长久使用，成为集实用与艺术于一体的文化瑰宝。', '传统扇子, 东方工艺, 文化美学, 夏日清凉', '2025-05-28 03:00:22.535323', '2025-05-28 03:00:22.535323');
INSERT INTO "public"."product_categories" VALUES ('1788419b-6f18-4467-808f-a73627806cb5', '风水琉璃', 'FENG SHUI LIULI COLLECTIBLE', '风水琉璃摆件系列，采用彩色琉璃材质制作，融合风水原理与艺术设计，为家居与办公环境带来美观与能量调节，成为收藏与装饰的理想选择。', 'ae6c4361-2f5f-4133-80bb-a7c1fcb70588', 'LEVEL_3', NULL, NULL, 't', 'f', 280, '风水琉璃 - 艺术与能量的和谐摆件', '风水琉璃摆件系列，采用优质彩色琉璃材质制作。我们的产品融合传统风水原理与现代艺术设计，展现独特的造型与色彩魅力。琉璃摆件种类丰富，包括水晶球、招财猫、转运轮、生肖造型等，每件作品都经过高温烧制、手工雕刻、精细打磨等多道工序，确保品质优良、光泽持久。在风水应用中，这些摆件能够调节气场、招财进宝、化解煞气，为环境带来正能量。同时，作为艺术品，它们提升空间美感，成为家居与办公装饰的亮点。我们的风水琉璃摆件适合收藏、赠送或作为风水调整工具，为您的生活空间增添和谐与美感，展现东方智慧与艺术创新的完美结合。', '风水琉璃, 能量调节, 艺术摆件, 招财装饰', '2025-05-28 03:00:22.536324', '2025-05-28 03:00:22.536324');
INSERT INTO "public"."product_categories" VALUES ('2e93a69c-6e21-41d7-9c9a-2031f7d7dbe6', '艺术品', 'ART_HOME_DECOR', '各类艺术品系列，包括绘画、雕塑、摄影作品等，展现艺术家的独特视角与文化深度，为您的空间带来艺术氛围，成为审美提升与文化传承的重要媒介。', 'ae6c4361-2f5f-4133-80bb-a7c1fcb70588', 'LEVEL_3', NULL, NULL, 't', 'f', 290, '艺术作品 - 审美提升的文化珍品', '各类艺术品系列，包括绘画、雕塑、摄影作品等多种形式。我们的艺术品来自世界各地的新兴与知名艺术家，展现多元文化视角与独特创作理念。每件作品都经过严格筛选，确保艺术价值与品质优良。这些艺术品不仅美化空间，更传递深刻的思想与情感，帮助观赏者拓展审美视野，感受不同文化的魅力。我们提供多种尺寸、材质、风格的选择，适合家居、办公室、商业空间等多种环境。购买艺术品不仅是装饰选择，更是参与文化传承、支持艺术创作的方式，为您的生活与工作空间注入灵魂与个性，成为文化对话与审美提升的重要媒介。', '艺术作品, 绘画雕塑, 审美提升, 文化传承', '2025-05-28 03:00:22.536324', '2025-05-28 03:00:22.536324');
INSERT INTO "public"."product_categories" VALUES ('fb9a8a15-1b74-4c7c-93de-d096d99c9e3c', '畅销商品', 'BEST SELLERS', '店内畅销商品精选，基于顾客喜爱与销售数据推荐，涵盖多个品类的热门产品，确保品质与价值，成为您选购的理想参考。', 'ae6c4361-2f5f-4133-80bb-a7c1fcb70588', 'LEVEL_3', NULL, NULL, 't', 'f', 300, '畅销商品 - 顾客喜爱的精选推荐', '店内畅销商品精选，基于长期销售数据与顾客反馈推荐。我们的畅销榜单涵盖珠宝首饰、冥想用品、藏式传统、服装服饰、家居装饰等多个品类，确保每件产品都经过市场验证，品质优良，价值出众。这些热门商品反映了顾客的喜好趋势与实际需求，从实用性强的日常用品到具有文化内涵的特色礼品，满足不同购买目的。我们定期更新畅销榜单，确保推荐的商品保持新鲜度与相关性。选择畅销商品，您将获得可靠的质量保障与满意的使用体验，同时也能发现被广泛认可的优质产品，成为您选购时的理想参考指南。', '畅销商品, 热门产品, 品质保障, 顾客推荐', '2025-05-28 03:00:22.536324', '2025-05-28 03:00:22.536324');
INSERT INTO "public"."product_categories" VALUES ('2da8dcb7-d0ed-41a0-bb38-ce78e8556e83', '家居装饰新品', 'NEW ARRIVAL-HOME DECOR', '最新到货的家居装饰商品，精选当季流行趋势与创新设计，为您的生活空间带来新鲜感与时尚元素，展现个性风格与现代美感。', 'ae6c4361-2f5f-4133-80bb-a7c1fcb70588', 'LEVEL_3', NULL, NULL, 't', 'f', 310, '家居装饰新品 - 时尚趋势的前沿选择', '最新到货的家居装饰商品系列，精选当季流行趋势与创新设计。我们的新品涵盖香薰炉、装饰画、摆件、储物盒、纺织品等多种类型，采用优质材料与精湛工艺制作，展现个性风格与现代美感。每件产品都经过趋势研究与精心挑选，确保符合当代审美与生活方式需求。新品装饰品为您的生活空间带来新鲜感，成为更新家居氛围的理想选择。我们定期推出新品，帮助您紧跟时尚潮流，打造独特而舒适的居住环境。无论是整体风格改造还是局部点缀，都能找到合适的商品，展现您的生活品味与个性主张。', '家居装饰新品, 流行趋势, 创新设计, 时尚元素', '2025-05-28 03:00:22.537831', '2025-05-28 03:00:22.537831');
INSERT INTO "public"."product_categories" VALUES ('8a98ac0b-b89c-42df-9358-0440c264d2fc', '墙面艺术', 'WALL_ART', '墙面装饰艺术系列，包括象征符号挂画、藏式经幡、唐卡等，展现文化深度与视觉美感，为室内空间增添艺术气息与精神氛围，成为墙面装饰的理想选择。', '1bc893b2-5227-4cd2-871d-10cdf3b89da4', 'LEVEL_2', NULL, NULL, 't', 'f', 30, '墙面艺术 - 文化深度的视觉享受', '墙面装饰艺术系列，包括象征符号挂画、藏式经幡、唐卡、风景画等多种类型。我们的墙面艺术品展现丰富文化内涵与视觉美感，采用优质材料如丝绸、棉麻、宣纸、亚克力等制作，确保色彩鲜艳、质感优良、持久耐用。这些装饰品不仅美化墙面，更传递深刻的精神价值与文化故事，为室内空间增添艺术气息与精神氛围。例如，藏式经幡随风飘动传播祝福，唐卡展现佛教智慧，象征符号挂画表达个人信念。我们的墙面艺术适合各种空间，从客厅、卧室到冥想室、办公室，帮助您打造富有个性与文化深度的视觉焦点，成为连接物质空间与精神世界的桥梁。', '墙面装饰, 象征符号, 藏式经幡, 唐卡艺术', '2025-05-28 03:00:22.538836', '2025-05-28 03:00:22.538836');
INSERT INTO "public"."product_categories" VALUES ('05315d10-2e09-4b44-bfb9-826358b298e0', '象征符号墙面', 'MEANINGFUL SYMBOLS WALL', '象征符号墙面装饰系列，以艺术形式展现文化与精神符号，帮助表达个人信念与价值观，为室内空间带来意义与美感，成为视觉焦点与精神表达的载体。', '8a98ac0b-b89c-42df-9358-0440c264d2fc', 'LEVEL_3', NULL, NULL, 't', 'f', 300, '象征符号墙面 - 个人信念的视觉表达', '象征符号墙面装饰系列，以艺术形式展现文化与精神符号。我们的产品包括画布印刷、丝绸刺绣、金属浮雕、木质雕刻等多种形式，内容涵盖佛教符号（如八宝、六字真言）、印度教标志（如奥姆符号）、东方哲学元素（如阴阳、八卦）、西方神秘学图案等。这些装饰品帮助您表达个人信念与价值观，为室内空间带来深刻意义与美感。每个符号都附有详细的文化解释与悬挂建议，确保您正确理解其内涵。象征符号墙面装饰不仅美化空间，更成为精神对话的媒介，为您的生活带来持续的启示与力量，成为每日视觉焦点与心灵滋养的源泉。', '象征符号, 个人信念, 文化标志, 视觉表达', '2025-05-28 03:00:22.538836', '2025-05-28 03:00:22.538836');
INSERT INTO "public"."product_categories" VALUES ('0bb76b9a-0072-438d-83ed-a08822c36b1d', '艺术品', 'ART_WALL', '各类墙面艺术品系列，包括绘画、摄影、版画等，展现艺术家的独特视角与创意表达，提升空间的艺术氛围，成为审美提升与文化探索的窗口。', '8a98ac0b-b89c-42df-9358-0440c264d2fc', 'LEVEL_3', NULL, NULL, 't', 'f', 310, '墙面艺术品 - 独特视角的视觉享受', '各类墙面艺术品系列，包括绘画、摄影、版画、浮雕等多种形式。我们的艺术品来自全球艺术家，展现多元文化视角与创意表达。每件作品都经过精心挑选，确保艺术价值与品质优良。这些墙面装饰提升空间的艺术氛围，帮助观赏者进入艺术家创造的视觉世界，感受不同的情感与思想。我们提供多种尺寸、材质、风格的选择，适合各种室内环境。购买艺术品不仅是装饰选择，更是参与文化对话、支持艺术创作的方式，为您的空间带来独特个性与深度美感，开启审美提升与文化探索的旅程。', '墙面艺术品, 绘画摄影, 创意表达, 艺术氛围', '2025-05-28 03:00:22.539835', '2025-05-28 03:00:22.539835');
INSERT INTO "public"."product_categories" VALUES ('5ffbe027-28cc-4772-bc7d-b0eb580e38f7', '藏式经幡', 'TIBETAN PRAYER FLAGS', '藏式经幡墙面装饰系列，印有经文与吉祥图案的彩色布旗，随风飘动传播正能量，为环境增添神圣氛围与文化美感，成为独特的祈福象征。', '8a98ac0b-b89c-42df-9358-0440c264d2fc', 'LEVEL_3', NULL, NULL, 't', 'f', 320, '藏式经幡 - 随风传播的祈福象征', '藏式经幡墙面装饰系列，印有佛教经文与吉祥图案的彩色布旗。我们的经幡采用优质布料制作，色彩鲜艳持久，图案包括佛像、神兽、咒语等传统元素。经幡在藏族文化中象征神圣的祈祷，当它们随风飘动时 believed to spread spiritual messages and blessings。将经幡装饰在墙面上，不仅为环境增添神圣氛围与文化美感，更是一种参与藏族精神实践的方式。我们的经幡提供多种尺寸与长度选择，适合阳台、庭院、室内悬挂等多种场合。每套经幡都附有详细的使用指南与文化背景说明，帮助您深入了解其意义，正确悬挂以获得最佳效果，为您的空间带来和谐与安宁。', '藏式经幡, 祈福象征, 能量传播, 文化装饰', '2025-05-28 03:00:22.539835', '2025-05-28 03:00:22.539835');
INSERT INTO "public"."product_categories" VALUES ('f70cb395-36ee-45eb-9c24-863dde4390e8', '唐卡绘画', 'THANGKA PAINTINGS', '传统唐卡绘画系列，以矿物颜料绘制佛像与藏族神话，展现精湛的绘画技艺与深厚的精神内涵，是藏族艺术的珍品，具有收藏与装饰价值。', '8a98ac0b-b89c-42df-9358-0440c264d2fc', 'LEVEL_3', NULL, NULL, 't', 'f', 330, '唐卡绘画 - 藏族艺术的精神珍品', '传统唐卡绘画系列，以矿物颜料精心绘制佛像与藏族神话场景。我们的唐卡由经验丰富的画师手工制作，遵循千年传统工艺，使用金箔、银箔、宝石粉末等珍贵材料，确保色彩鲜艳持久、线条细腻流畅。每幅唐卡都蕴含深厚的宗教意义与精神价值，展现佛菩萨的神圣形象与藏族宇宙观。唐卡不仅是艺术品，更是修行辅助工具，帮助观想与冥想。我们提供多种尺寸与题材选择，包括佛像、菩萨、护法、本尊等，适合家居供奉、寺庙装饰或艺术收藏。每幅唐卡都附有详细背景说明与保养指南，帮助您深入了解其文化内涵，珍藏这份来自雪域高原的艺术瑰宝，为生活空间带来神圣氛围与文化深度。', '唐卡绘画, 藏族艺术, 佛像唐卡, 艺术收藏', '2025-05-28 03:00:22.540841', '2025-05-28 03:00:22.540841');
INSERT INTO "public"."product_categories" VALUES ('6a3648ce-5e62-457d-926f-1b46e7d9da46', '风铃与铜铃', 'BELLS + CHIMES', '风铃与铜铃墙面装饰系列，以金属材质制作，通过风的吹动产生悦耳声音，帮助净化空间，创造和谐氛围，成为听觉与视觉的双重享受。', '8a98ac0b-b89c-42df-9358-0440c264d2fc', 'LEVEL_3', NULL, NULL, 't', 'f', 340, '风铃与铜铃 - 和谐声音的墙面装饰', '风铃与铜铃墙面装饰系列，以金属材质精心制作。我们的产品包括传统风铃、管铃、铜铃等多种类型，设计融合文化元素与现代美感。风铃通过风的吹动产生悦耳声音，帮助净化空间、提升能量、创造和谐氛围。部分款式还可作为门帘或挂饰使用，兼具实用与装饰功能。风铃与铜铃不仅带来听觉享受，其金属光泽与精致造型也为墙面增添视觉美感。我们的风铃采用优质材料，确保声音清脆悠扬、结构稳固耐用。每件作品都经过声音调试与质量检验，确保您获得最佳的听觉与视觉体验，为您的室外与室内空间带来自然能量与艺术氛围，成为连接声音疗愈与家居装饰的完美媒介。', '风铃铜铃, 和谐声音, 空间净化, 视听享受', '2025-05-28 03:00:22.541835', '2025-05-28 03:00:22.541835');
INSERT INTO "public"."product_categories" VALUES ('f7d3fef4-7fb6-4e13-8c2d-8c433e353743', '为女性', 'FOR WOMEN', '专为女性设计的礼物系列，融合优雅与实用，涵盖珠宝、服饰、冥想用品等多种选择，展现对女性特质的深刻理解，成为表达关怀与欣赏的理想方式。', '046970d6-f118-49bd-92b0-382f407f9cc8', 'LEVEL_2', NULL, NULL, 't', 'f', 10, '女性礼物系列 - 优雅实用的贴心选择', '专为女性设计的礼物系列，融合优雅与实用元素。我们的女性礼物涵盖珠宝首饰、舒适服装、精美的冥想用品等多种品类，每件礼品都经过精心挑选，展现对女性特质的深刻理解。珠宝系列展现女性的柔美与魅力，服装系列注重舒适与风格，冥想用品帮助女性在繁忙生活中找到平静。这些礼物不仅是物质赠送，更是对女性内在价值的欣赏与尊重，成为表达关怀、爱意与敬意的理想选择，让每一位女性都感受到特别的对待与温暖的心意。', '女性礼物, 珠宝首饰, 舒适服装, 冥想用品', '2025-05-28 03:00:22.542834', '2025-05-28 03:00:22.542834');
INSERT INTO "public"."product_categories" VALUES ('726e905f-253f-4e58-bc3d-828df2ae5fbc', '为男性', 'FOR MEN', '专为男性设计的礼物系列，融合简约与力量感，提供珠宝、服饰、实用配饰等多种选择，展现阳刚气质与品味，成为表达尊重与欣赏的理想方式。', '046970d6-f118-49bd-92b0-382f407f9cc8', 'LEVEL_2', NULL, NULL, 't', 'f', 20, '男性礼物系列 - 简约力量的品味选择', '专为男性设计的礼物系列，融合简约设计与力量感。我们的男性礼物包括精致珠宝、舒适服装、实用配饰等多种选择，展现阳刚气质与高雅品味。珠宝系列注重细节与质感，服装系列强调合身与舒适，实用配饰如钱包、皮带、钥匙链等满足日常需求。这些礼物不仅是实用物品，更是对男性内在价值的认可与尊重，成为表达关怀、感谢与敬意的理想方式。无论是父亲、丈夫、朋友还是同事，都能在我们的系列中找到合适的礼物，传递您的心意与祝福。', '男性礼物, 精致珠宝, 舒适服装, 实用配饰', '2025-05-28 03:00:22.542834', '2025-05-28 03:00:22.542834');
INSERT INTO "public"."product_categories" VALUES ('5d0f52db-3b7f-4431-9d2a-bed455939904', '为情侣', 'FOR COUPLE', '专为情侣设计的礼物系列，展现浪漫与甜蜜，包括对戒、情侣装、双人冥想套装等，帮助表达爱意与承诺，成为关系升温与纪念时刻的理想选择。', '046970d6-f118-49bd-92b0-382f407f9cc8', 'LEVEL_2', NULL, NULL, 't', 'f', 30, '情侣礼物系列 - 浪漫甜蜜的爱情表达', '专为情侣设计的礼物系列，展现浪漫与甜蜜元素。我们的礼物包括对戒、情侣项链、情侣手链等珠宝系列，展现永恒的爱与承诺；情侣装如T恤、外套等展现默契与统一；双人冥想套装帮助情侣在精神层面建立更深连接。每件礼品都经过精心设计，注重细节与品质，为特别的日子增添难忘回忆。这些礼物不仅是物质赠送，更是情感交流与爱意表达的方式，帮助您向伴侣传递深刻的情感与珍惜之情，成为关系升温与纪念时刻的理想选择。', '情侣礼物, 对戒项链, 情侣装, 双人套装', '2025-05-28 03:00:22.543835', '2025-05-28 03:00:22.543835');
INSERT INTO "public"."product_categories" VALUES ('1d67e36f-5164-44ef-b476-f6954c707563', '个性化礼物', 'PERSONALIZED GIFTS', '个性化定制礼物系列，提供刻字、图案定制服务，打造独一无二的礼品，展现专属心意与特别记忆，成为表达独特情感的理想选择。', '046970d6-f118-49bd-92b0-382f407f9cc8', 'LEVEL_2', NULL, NULL, 't', 'f', 40, '个性化礼物 - 独一无二的情感表达', '个性化定制礼物系列，提供刻字、图案设计、材料选择等多种定制服务。我们的产品包括珠宝首饰、饰品盒、服装、冥想用品等，帮助您打造独一无二的礼品。每件礼品都经过精心制作，确保定制内容精确呈现，展现专属心意与特别记忆。个性化礼物不仅是物质赠送，更是情感交流的深度体现，能够让接收者感受到您的用心与关怀。无论是纪念日、生日还是特殊场合，定制礼物都能成为表达独特情感、传递珍贵记忆的理想方式，让每一份礼物都具有特殊意义与永恒价值。', '个性化定制, 刻字服务, 独特礼品, 情感表达', '2025-05-28 03:00:22.543835', '2025-05-28 03:00:22.543835');
INSERT INTO "public"."product_categories" VALUES ('7f149e82-5599-46e6-ad99-853bdf52c729', '礼物套装', 'GIFT SET', '精选礼物套装系列，精心搭配多种商品，满足不同场合需求，提供便捷的送礼选择，展现全方位的关怀与品味，成为一站式礼物解决方案。', '046970d6-f118-49bd-92b0-382f407f9cc8', 'LEVEL_2', NULL, NULL, 't', 'f', 50, '礼物套装 - 精心搭配的全方位选择', '精选礼物套装系列，精心搭配多种商品，满足生日、节庆、纪念日等不同场合需求。我们的套装包括珠宝组合、冥想用品套装、香薰礼盒、服装配饰组合等多种类型，每套礼物都经过专业搭配，确保实用与美观并存。礼物套装的优势在于一站式解决您的送礼需求，节省挑选时间，同时通过精心组合展现全方位的关怀与品味。每套礼物都采用精美包装，提升整体质感，成为表达心意的理想选择。无论是家庭聚会、商务往来还是朋友间的情谊表达，都能找到合适的礼物套装，传递您的温暖与祝福。', '礼物套装, 精心搭配, 多样商品, 送礼选择', '2025-05-28 03:00:22.544842', '2025-05-28 03:00:22.544842');
INSERT INTO "public"."product_categories" VALUES ('1044f952-b753-45bf-8f18-a7cca16e6cc0', '首饰盒', 'JEWELRY CASE', '精美首饰盒系列，采用优质材料制作，设计优雅实用，帮助收纳与展示珠宝，成为赠送首饰的理想配套，展现精致与呵护的心意。', '046970d6-f118-49bd-92b0-382f407f9cc8', 'LEVEL_2', NULL, NULL, 't', 'f', 60, '首饰盒 - 精致收纳的珠宝伴侣', '精美首饰盒系列，采用优质木材、皮革、丝绸等材料制作，展现优雅设计与实用功能。我们的首饰盒提供多种尺寸与风格选择，从简约现代到复古奢华，满足不同审美需求。内部结构精心设计，包括分隔层、抽屉、悬挂空间等，确保各类珠宝（戒指、耳环、项链、手链等）都能得到妥善收纳与保护。首饰盒不仅是实用物品，更是赠送珠宝的理想配套，展现您的精致与呵护之心。我们还提供定制服务，如刻字、专属标志等，让首饰盒成为具有纪念意义的礼物。无论是作为自我收藏还是赠送他人，首饰盒都将成为珠宝的完美归宿，增添使用时的愉悦体验。', '首饰盒, 收纳展示, 精致设计, 定制服务', '2025-05-28 03:00:22.545836', '2025-05-28 03:00:22.545836');
INSERT INTO "public"."product_categories" VALUES ('9036b668-0295-4d9d-9117-8418e939e36f', '电子礼券', 'DIGITAL GIFT CERTIFICATE', '电子礼券系列，提供便捷的数字礼物选择，可自定义金额与祝福语，通过邮件或短信发送，成为快速传递心意的理想方式，适合各种紧急与特殊送礼需求。', '046970d6-f118-49bd-92b0-382f407f9cc8', 'LEVEL_2', NULL, NULL, 't', 'f', 70, '电子礼券 - 快捷方便的心意传递', '电子礼券系列，提供便捷的数字礼物选择。我们的礼券允许您自定义金额、选择祝福模板、添加个人留言，通过邮件或短信即时发送给接收者。电子礼券适用于各种场合，如生日、节日、纪念日、商务馈赠等，尤其适合紧急送礼需求或无法当面赠送的情况。接收者可在礼券有效期内自由选购网站上的任何商品，确保礼物符合其个人喜好。电子礼券不仅环保便捷，更展现出送礼者的 thoughtful 与现代化，成为快速传递心意的理想方式。我们提供多种设计精美的礼券模板，确保您的心意得到完美表达。', '电子礼券, 数字礼物, 自定义金额, 即时发送', '2025-05-28 03:00:22.546842', '2025-05-28 03:00:22.546842');
INSERT INTO "public"."product_categories" VALUES ('c2602244-50d1-43f0-b2a5-5929baa487e0', '藏式用品', 'TIBET', '探索丰富多样的藏式传统用品，从精美的藏式饰品到神圣的修行工具，每一件都蕴含深厚的文化底蕴与精神价值，带您领略雪域高原的独特魅力。', NULL, 'LEVEL_1', NULL, NULL, 't', 'f', 1, '藏式用品 - 传统与精神的完美融合', '探索丰富多样的藏式传统用品系列，从精美的藏式饰品到神圣的修行工具，每一件都蕴含深厚的文化底蕴与精神价值。我们的藏式用品经过精心挑选，确保材质优良与工艺精湛，展现雪域高原的独特魅力。无论是用于个人修行、家居装饰还是作为珍贵礼物，这些用品都能为您带来独特的文化体验与精神启迪，连接古老智慧与现代生活，成为您了解藏文化的理想窗口。', '藏式用品, 藏式饰品, 修行工具, 藏文化', '2025-05-28 03:00:22.495944', '2025-05-30 11:11:28.688933');
INSERT INTO "public"."product_categories" VALUES ('046970d6-f118-49bd-92b0-382f407f9cc8', '礼物', 'GIFTS', '精心挑选的礼物系列，根据接收者与场合分类，包括个性化定制、首饰盒、电子礼券等多种选择，为您的送礼需求提供全方位解决方案，传递心意与文化价值。', NULL, 'LEVEL_1', NULL, NULL, 't', 'f', 2, '特色礼物系列 - 传递心意与文化价值', '精心挑选的礼物系列，根据接收者与场合分类。我们的礼物包括为女性、男性、情侣设计的专门系列，个性化定制服务满足独特需求，首饰盒与电子礼券提供更多便利选择。每件礼品都融合优质材质与精美设计，展现文化深度与艺术美感，确保您的心意得到完美表达。无论是生日、纪念日、节庆还是日常惊喜，我们都能帮助您找到合适的礼物，传递情感与祝福，成为您表达关怀的理想方式。', '特色礼物, 个性化定制, 首饰盒, 电子礼券', '2025-05-28 03:00:22.541835', '2025-05-30 11:11:45.835914');
INSERT INTO "public"."product_categories" VALUES ('792e259e-713e-4f1a-9bd5-1b84c3567ff9', '热门趋势', 'TRENDING', '探索当前最受欢迎的珠宝首饰系列，包括蛇年主题、红绳饰品、翡翠珠宝等热门款式，展现最新潮流趋势与文化元素，满足您对时尚与个性的追求。', NULL, 'LEVEL_1', NULL, NULL, 't', 'f', 3, '热门趋势珠宝 - 探索最新潮流款式', '探索当前最受欢迎的珠宝首饰系列，从蛇年主题饰品到经典红绳款式，从珍贵翡翠到时尚金属系列。我们的热门趋势板块汇集最新潮流元素与文化主题，精心挑选每一件作品，展现独特设计与卓越工艺。无论是追随时尚步伐还是寻找个性表达，这里都能满足您的需求，为您的装扮增添亮点与话题性，成为潮流前沿的理想选择。', '热门珠宝, 趋势饰品, 蛇年主题, 红绳珠宝', '2025-05-28 03:00:22.486431', '2025-05-30 11:11:59.401194');
INSERT INTO "public"."product_categories" VALUES ('32b50225-0657-4de3-ae51-959f1de68282', '念珠', 'MALA_BEADS', '探索精美的Mala念珠系列，包括菩提子、木质、宝石等多种材质的念珠，每一件都经过精心制作，不仅适用于冥想修行，更是展现个人风格的独特配饰。', NULL, 'LEVEL_1', NULL, NULL, 't', 'f', 4, 'Mala Beads - 精美念珠系列', '探索精美的Mala念珠系列，包括菩提子、木质、宝石等多种材质。这些念珠不仅适用于冥想修行，帮助集中注意力与平衡能量，更是展现个人风格的独特配饰，为您的日常生活增添精神气息与时尚感。', 'Mala念珠, 菩提子念珠, 木质念珠, 宝石念珠, 冥想配饰', '2025-05-28 03:00:22.466411', '2025-05-30 11:12:17.06845');
INSERT INTO "public"."product_categories" VALUES ('1bc893b2-5227-4cd2-871d-10cdf3b89da4', '家宅饰品', 'HOME_DECOR', '家宅饰品', NULL, 'LEVEL_1', NULL, NULL, 't', 'f', 6, '家宅饰品', '家宅饰品', '家宅饰品', '2025-05-28 03:00:22.524815', '2025-05-30 11:12:32.367255');
INSERT INTO "public"."product_categories" VALUES ('00e865af-c686-404a-8760-dbb3bca5ecbc', '服装', 'APPAREL', '探索专为冥想、瑜伽和日常穿着设计的舒适服装系列，融合传统元素与现代风格，展现自然美感与文化深度，为您的身心实践和日常生活提供理想着装选择。', NULL, 'LEVEL_1', NULL, NULL, 't', 'f', 7, '冥想与瑜伽服装 - 传统与现代的融合', '探索专为冥想、瑜伽和日常穿着设计的舒适服装系列。我们的服装融合传统元素与现代风格，采用有机棉、亚麻、竹纤维等天然面料制作，确保透气性与耐用性。每件作品都经过精心设计，展现自然美感与文化深度，帮助您在练习中自由移动，在日常生活中保持舒适与风格。无论是寻找瑜伽服饰、冥想长袍还是日常休闲装，我们的服装系列都能满足您的需求，成为您身心实践和时尚表达的理想选择。', '冥想服装, 瑜伽服饰, 有机棉服装, 文化风格', '2025-05-28 03:00:22.505161', '2025-05-30 11:12:39.977756');

-- ----------------------------
-- Table structure for product_category
-- ----------------------------
DROP TABLE IF EXISTS "public"."product_category";
CREATE TABLE "public"."product_category" (
  "product_id" uuid NOT NULL,
  "category_id" uuid NOT NULL
)
;

-- ----------------------------
-- Records of product_category
-- ----------------------------
INSERT INTO "public"."product_category" VALUES ('8412d590-9bf6-47c9-a5fc-302f1847513c', 'f7d3fef4-7fb6-4e13-8c2d-8c433e353743');
INSERT INTO "public"."product_category" VALUES ('8412d590-9bf6-47c9-a5fc-302f1847513c', '5d0f52db-3b7f-4431-9d2a-bed455939904');
INSERT INTO "public"."product_category" VALUES ('8412d590-9bf6-47c9-a5fc-302f1847513c', 'a80a2ae9-814d-4577-8f23-ea959c891462');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '0b250eab-a67a-4d50-bdfc-2750efcd6142');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '3c9af24e-e571-431a-bd5b-00f1d79b07cc');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '48744cc6-48df-48b4-9539-f8699185a13a');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'b1bcf436-aa43-41a7-9c22-79b2f990efff');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'd93ed170-8f13-4e14-830c-4e616a23c355');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '0781d07f-d69f-4149-8288-07d79041e0f1');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '8e26b1a7-8d3a-4f57-b14c-07558036ae6c');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '7d18cc78-50b1-457f-a588-2694473582b1');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'b9f93620-7790-429d-9c94-25107f7d196c');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'a2f37ca8-e1b1-4969-abb1-2af26e9ffc62');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'e61707f0-a0ae-4662-a3b6-3e5354e0587f');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '82300a7e-38a5-4ca7-9998-2b14812abf0c');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'b7aeb673-102c-41d5-94f3-f2d05e0d4c81');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '60904db1-acc7-47ea-88eb-bbbe9db46162');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '16264aae-052d-4479-be0c-fc0b2ef169aa');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'd8733286-c141-496c-8b55-0ef2710accd5');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'f719f82c-39b4-4a61-8884-058aebea1c7f');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'e2041c77-4380-4b2a-93a6-f4dcf3ceb3b6');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'd8b08a2b-d034-4131-acb3-477277c6d82a');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'cad2a041-6eaf-4f39-bef4-2ade3a55d77d');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'b29c845c-07de-408d-94bf-fb682c9921f8');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'd739d9ce-3361-40f8-a0ca-c6e45af0b40f');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'd5ff8b3b-ed80-484c-9d5f-12cf5273c94e');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '846e749f-781f-4aff-8eff-0426b20d0de8');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '9e968995-d903-42c7-aaab-0f68a0c9d920');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'f10b711e-742f-404d-813f-0c2ca8542ff2');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'caf67522-2aed-4394-ad89-1d7ffc447518');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '59ccefa3-b1f3-4b0b-9587-e428ba6a205d');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '05ab7b51-b250-4bbd-9cd2-bb39baf5842e');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '8e75b808-6952-465c-88a9-a5babf0f14c3');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '38d52275-417b-4327-86dc-22fad45e0301');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '7b1b08fb-b5ba-4280-9e80-afb2ce9e439a');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'af046d5b-65f2-4cef-99c3-b0723c142b50');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '2dba15fb-c40b-471b-8192-40552834bc90');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '226f6a96-b492-442f-9a26-f3b6698a5653');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'ef4056e2-0c63-4f44-8f64-bf4a9b66d56d');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'cb55c3b8-a243-4e26-8e7c-9f446faf9fe8');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'd8d198c2-c5fd-484e-a4d2-d0e83c5c034d');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '196c8399-4eb7-47dc-9db1-2cf06527f24c');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '5597ec2d-7c51-4ed7-ad2b-484275f0a0c0');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '0c448a28-1e50-4854-866b-f046e22d0d58');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'c532521d-7228-43ba-a95a-57c0cc2fd1d5');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '4c88f233-12d9-4718-b52e-9bedbe5685fb');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '2b39d691-793e-47d9-ae37-adb468fd7d1c');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'd7f3591b-59d4-41d3-a9d8-b21120718307');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '95875f70-2d10-47f4-8aa5-b43e8ee7eeae');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '6c14399d-4d4d-4eb9-8f9e-0ed36241dce8');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'f6867f3e-5cba-4721-a8d0-17d1a82332ca');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'eeee67a5-15b8-4c5e-914f-a4b7b7a8160e');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'bf42e9fa-ccaa-4255-9c14-ca52919dfe13');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '7f438404-11b4-493d-b26d-fc68b64c4beb');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '45969b85-fb2b-479a-93d5-2e97f3e28db5');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'ae9c84d4-2d44-4987-9695-69f81dba90de');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'f38e7690-4f9c-4aea-b82d-55697e4c342b');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'a946fd9d-44a9-4ca8-b197-86d0fb3f99c3');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '0611edfb-ec07-46ed-ae49-7b17caba9826');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'ff51bf02-6f4b-4337-ba76-b5c034ad616e');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '6c858d52-05f1-4629-bcc9-461594625ea0');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '3ffb427b-f473-40bf-9ece-3f4e927bb217');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '0243e37b-9373-40e0-b9ac-82f5bd79d01e');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'd7e4bb4b-e20d-4312-9350-065ebda9dc6a');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '906adfdf-8b62-48bc-8c3d-80e0dd3fc70f');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '7f0a0b8e-70ed-4600-bac5-7ad280ac6191');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '96cd6df4-9e77-4b0c-b0db-5d2f8b9c9fea');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '5aa94d1c-036f-44c0-a173-9a8683634f44');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '10a0646e-d445-44c0-bbeb-98b257b9de1e');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '0727c619-f8e7-407b-a290-e3cf6a8ef673');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '3142edbc-3764-476f-b03b-28511018ddc8');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '87276629-459e-430f-833f-ed4112f15fa5');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '7a14b046-e837-4219-b2c8-e3ced0e147d0');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'b5eca328-9a1a-4164-9441-a8dbcd16cd94');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'a8008b40-cb3c-497a-baec-394c4fe102a4');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '6e290f22-b73e-481e-bc4d-50b6a212c515');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '015be9b3-a974-44dd-92c3-341e71b8a0c8');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '8ee2997b-2ce5-40b7-a116-5e420ae3391b');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '9098463d-e301-426e-9519-adbe7540adb9');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '5011327d-fdb3-4e9e-ba67-340e39307160');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'f3857cd3-cfac-4127-add2-11be4fbddbed');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '3efb29e7-2d0c-4a99-9c0e-02f804586afd');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'b2532dc7-306d-436c-85ea-920f2becd4e5');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'e436becc-4632-4c9b-865b-e52eeaa4d823');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'b388fe53-5dd0-4a86-b99c-c4c5533637d3');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '4db72b73-948b-4748-afc9-595fa95dc3f1');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '4f5348d7-4cc5-45bf-b2fc-b11c0aca9905');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'a80a2ae9-814d-4577-8f23-ea959c891462');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'b2f1bb92-99c6-43b6-97ef-20dca3f4165d');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '616bd56e-606f-4c49-9e51-491fd6f2bb65');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '50696737-a64a-4761-94b6-c3224dabd486');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '1b0946ee-35c6-470f-b72e-817d02091bcd');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'd93f22af-8151-4358-8dff-264b123fa6be');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '6bc7b47e-4179-4cf2-a5bb-c4ea090ef297');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '62ce3ff8-fe78-4775-80c4-9ab23844def4');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '10df813e-1b02-49d5-8389-0915c992c53c');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'c5f96dac-d07a-4a7f-91ad-28e06c216215');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '4aeb9171-2dce-486e-b586-9f7536c8e889');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'f39d7472-164b-4860-b4c7-51e0b00684cb');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '8093514d-3e58-45cc-812f-1c4b04f9c904');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'f7ff8396-f88d-49db-b1f2-dc6fad6fe96f');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '2445fe19-b637-4d6c-898d-4824651278f6');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'a10e684e-553f-4200-9f07-311dbead4a88');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '2ffc2508-b703-4831-9c0b-f96b5c5539dd');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '4d78477c-c274-42c5-8838-9d9a8cb206e2');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'ba8caffe-dd48-4fe2-9cc8-3a9a3abfdd5a');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '7be43317-35eb-418e-a0da-292c8b67b49d');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'ad036486-f2c8-4be1-9c23-36def611da15');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'd109f10f-a9d9-465e-8a09-47df8e9fa1e0');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'd2be0199-66ee-4b0e-a94e-dc1611df8177');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '4e5197d9-b8c8-4931-8c00-bef26f35a6b6');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '7dd2d24e-4c4a-4ec8-9fab-33064141dbda');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '3bddb143-125c-4e04-b0a7-099f456b1472');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'eb2f2864-0eaa-408a-9577-2989ad49d147');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '5303b8d1-6c1a-423b-a2c3-d928350e3d11');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'bb138143-13a0-4b6e-ae32-1dbc0a83a576');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '16f5bd13-3bb4-4eab-8a50-bf68a8b78cf0');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '3a70219b-6a08-469c-a405-e02bf1ee2cf2');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '8cea7dd7-75e3-47d7-9589-976de815ec24');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'e424c6af-03a1-4572-bd34-31a547c8df13');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '83e5dfdd-1bc1-481f-8dc2-e3d8884730a2');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '3524304d-c372-4449-8743-562a47903692');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '365a40d4-a193-4a42-b756-1bd97d6ce679');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'f61fdd9d-346b-4bf2-8680-ea4eeee167db');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '4a9e3456-33a2-4615-9b7e-fa6301c6cf17');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'd4dbad47-4e7f-448e-be7b-ec461a4f2f5d');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '39cad863-d669-4cad-9d48-ef281329d233');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '1fbe1c95-d916-4676-9514-e8e95ca7dd78');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '0afd7191-46da-42c5-ab2e-33757a7dec37');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'a73ff6e6-cab0-4829-85b5-5e98c11ce7ae');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '4841d455-7b84-47ed-a3d2-93d5e42d407c');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '70b7b4d8-8e9d-4c56-85dd-772c06b2fe42');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'd17378c1-5046-4360-99ee-75182a26e5ec');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '09c86466-821a-44b2-9210-36a618d08a78');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '0fb693d4-66d7-4633-9d09-1473c3038f6e');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '05e3d800-057d-497a-8916-e406dae5cfea');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '07ae0908-da25-43cf-b1f1-82c3123b1ebe');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '8822a91d-d5e3-415e-b245-3725b3598b79');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'be178bf7-c03b-48d8-9602-05b906ea6cba');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '648bd9e4-f161-4b86-9aaa-46a9486d5acf');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'ae6c4361-2f5f-4133-80bb-a7c1fcb70588');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'ef5e5203-97df-468d-bfa0-2a3d64f4c1ca');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'c939f87d-6cd9-405a-9e7f-8b74ae1e2797');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '7604d919-b3dc-491f-bf9c-89d6657e7cd1');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '5894bde9-4f8b-48d7-871f-94e3d4e9641b');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'a02c92e7-45c0-4543-abbb-3d20ca466f41');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'df2e0873-6539-47e8-9c4d-61c342204336');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '34dde886-3bee-402f-8f99-652d14634800');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '7c38698d-7db3-48e5-882f-76aee3bfd999');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '1788419b-6f18-4467-808f-a73627806cb5');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '2e93a69c-6e21-41d7-9c9a-2031f7d7dbe6');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'fb9a8a15-1b74-4c7c-93de-d096d99c9e3c');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '2da8dcb7-d0ed-41a0-bb38-ce78e8556e83');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '8a98ac0b-b89c-42df-9358-0440c264d2fc');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '05315d10-2e09-4b44-bfb9-826358b298e0');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '0bb76b9a-0072-438d-83ed-a08822c36b1d');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '5ffbe027-28cc-4772-bc7d-b0eb580e38f7');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'f70cb395-36ee-45eb-9c24-863dde4390e8');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '6a3648ce-5e62-457d-926f-1b46e7d9da46');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'f7d3fef4-7fb6-4e13-8c2d-8c433e353743');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '726e905f-253f-4e58-bc3d-828df2ae5fbc');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '5d0f52db-3b7f-4431-9d2a-bed455939904');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '1d67e36f-5164-44ef-b476-f6954c707563');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '7f149e82-5599-46e6-ad99-853bdf52c729');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '1044f952-b753-45bf-8f18-a7cca16e6cc0');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '9036b668-0295-4d9d-9117-8418e939e36f');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'c2602244-50d1-43f0-b2a5-5929baa487e0');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '046970d6-f118-49bd-92b0-382f407f9cc8');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '792e259e-713e-4f1a-9bd5-1b84c3567ff9');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '32b50225-0657-4de3-ae51-959f1de68282');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '1bc893b2-5227-4cd2-871d-10cdf3b89da4');
INSERT INTO "public"."product_category" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', '00e865af-c686-404a-8760-dbb3bca5ecbc');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '0b250eab-a67a-4d50-bdfc-2750efcd6142');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '3c9af24e-e571-431a-bd5b-00f1d79b07cc');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '48744cc6-48df-48b4-9539-f8699185a13a');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'b1bcf436-aa43-41a7-9c22-79b2f990efff');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'd93ed170-8f13-4e14-830c-4e616a23c355');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '0781d07f-d69f-4149-8288-07d79041e0f1');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '8e26b1a7-8d3a-4f57-b14c-07558036ae6c');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '7d18cc78-50b1-457f-a588-2694473582b1');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'b9f93620-7790-429d-9c94-25107f7d196c');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'a2f37ca8-e1b1-4969-abb1-2af26e9ffc62');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'e61707f0-a0ae-4662-a3b6-3e5354e0587f');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '82300a7e-38a5-4ca7-9998-2b14812abf0c');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'b7aeb673-102c-41d5-94f3-f2d05e0d4c81');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '60904db1-acc7-47ea-88eb-bbbe9db46162');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '16264aae-052d-4479-be0c-fc0b2ef169aa');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'd8733286-c141-496c-8b55-0ef2710accd5');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'f719f82c-39b4-4a61-8884-058aebea1c7f');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'e2041c77-4380-4b2a-93a6-f4dcf3ceb3b6');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'd8b08a2b-d034-4131-acb3-477277c6d82a');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'cad2a041-6eaf-4f39-bef4-2ade3a55d77d');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'b29c845c-07de-408d-94bf-fb682c9921f8');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'd739d9ce-3361-40f8-a0ca-c6e45af0b40f');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'd5ff8b3b-ed80-484c-9d5f-12cf5273c94e');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '846e749f-781f-4aff-8eff-0426b20d0de8');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '9e968995-d903-42c7-aaab-0f68a0c9d920');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'f10b711e-742f-404d-813f-0c2ca8542ff2');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'caf67522-2aed-4394-ad89-1d7ffc447518');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '59ccefa3-b1f3-4b0b-9587-e428ba6a205d');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '05ab7b51-b250-4bbd-9cd2-bb39baf5842e');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '8e75b808-6952-465c-88a9-a5babf0f14c3');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '38d52275-417b-4327-86dc-22fad45e0301');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '7b1b08fb-b5ba-4280-9e80-afb2ce9e439a');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'af046d5b-65f2-4cef-99c3-b0723c142b50');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '2dba15fb-c40b-471b-8192-40552834bc90');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '226f6a96-b492-442f-9a26-f3b6698a5653');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'ef4056e2-0c63-4f44-8f64-bf4a9b66d56d');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'cb55c3b8-a243-4e26-8e7c-9f446faf9fe8');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'd8d198c2-c5fd-484e-a4d2-d0e83c5c034d');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '196c8399-4eb7-47dc-9db1-2cf06527f24c');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '5597ec2d-7c51-4ed7-ad2b-484275f0a0c0');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '0c448a28-1e50-4854-866b-f046e22d0d58');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'c532521d-7228-43ba-a95a-57c0cc2fd1d5');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '4c88f233-12d9-4718-b52e-9bedbe5685fb');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '2b39d691-793e-47d9-ae37-adb468fd7d1c');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'd7f3591b-59d4-41d3-a9d8-b21120718307');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '95875f70-2d10-47f4-8aa5-b43e8ee7eeae');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '6c14399d-4d4d-4eb9-8f9e-0ed36241dce8');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'f6867f3e-5cba-4721-a8d0-17d1a82332ca');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'eeee67a5-15b8-4c5e-914f-a4b7b7a8160e');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'bf42e9fa-ccaa-4255-9c14-ca52919dfe13');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '7f438404-11b4-493d-b26d-fc68b64c4beb');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '45969b85-fb2b-479a-93d5-2e97f3e28db5');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'ae9c84d4-2d44-4987-9695-69f81dba90de');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'f38e7690-4f9c-4aea-b82d-55697e4c342b');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'a946fd9d-44a9-4ca8-b197-86d0fb3f99c3');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '0611edfb-ec07-46ed-ae49-7b17caba9826');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'ff51bf02-6f4b-4337-ba76-b5c034ad616e');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '6c858d52-05f1-4629-bcc9-461594625ea0');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '3ffb427b-f473-40bf-9ece-3f4e927bb217');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '0243e37b-9373-40e0-b9ac-82f5bd79d01e');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'd7e4bb4b-e20d-4312-9350-065ebda9dc6a');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '906adfdf-8b62-48bc-8c3d-80e0dd3fc70f');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '7f0a0b8e-70ed-4600-bac5-7ad280ac6191');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '96cd6df4-9e77-4b0c-b0db-5d2f8b9c9fea');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '5aa94d1c-036f-44c0-a173-9a8683634f44');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '10a0646e-d445-44c0-bbeb-98b257b9de1e');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '0727c619-f8e7-407b-a290-e3cf6a8ef673');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '3142edbc-3764-476f-b03b-28511018ddc8');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '87276629-459e-430f-833f-ed4112f15fa5');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '7a14b046-e837-4219-b2c8-e3ced0e147d0');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'b5eca328-9a1a-4164-9441-a8dbcd16cd94');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'a8008b40-cb3c-497a-baec-394c4fe102a4');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '6e290f22-b73e-481e-bc4d-50b6a212c515');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '015be9b3-a974-44dd-92c3-341e71b8a0c8');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '8ee2997b-2ce5-40b7-a116-5e420ae3391b');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '9098463d-e301-426e-9519-adbe7540adb9');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '5011327d-fdb3-4e9e-ba67-340e39307160');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'f3857cd3-cfac-4127-add2-11be4fbddbed');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '3efb29e7-2d0c-4a99-9c0e-02f804586afd');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'b2532dc7-306d-436c-85ea-920f2becd4e5');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'e436becc-4632-4c9b-865b-e52eeaa4d823');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'b388fe53-5dd0-4a86-b99c-c4c5533637d3');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '4db72b73-948b-4748-afc9-595fa95dc3f1');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '4f5348d7-4cc5-45bf-b2fc-b11c0aca9905');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'a80a2ae9-814d-4577-8f23-ea959c891462');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'b2f1bb92-99c6-43b6-97ef-20dca3f4165d');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '616bd56e-606f-4c49-9e51-491fd6f2bb65');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '50696737-a64a-4761-94b6-c3224dabd486');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '1b0946ee-35c6-470f-b72e-817d02091bcd');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'd93f22af-8151-4358-8dff-264b123fa6be');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '6bc7b47e-4179-4cf2-a5bb-c4ea090ef297');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '62ce3ff8-fe78-4775-80c4-9ab23844def4');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '10df813e-1b02-49d5-8389-0915c992c53c');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'c5f96dac-d07a-4a7f-91ad-28e06c216215');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '4aeb9171-2dce-486e-b586-9f7536c8e889');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'f39d7472-164b-4860-b4c7-51e0b00684cb');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '8093514d-3e58-45cc-812f-1c4b04f9c904');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'f7ff8396-f88d-49db-b1f2-dc6fad6fe96f');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '2445fe19-b637-4d6c-898d-4824651278f6');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'a10e684e-553f-4200-9f07-311dbead4a88');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '2ffc2508-b703-4831-9c0b-f96b5c5539dd');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '4d78477c-c274-42c5-8838-9d9a8cb206e2');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'ba8caffe-dd48-4fe2-9cc8-3a9a3abfdd5a');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '7be43317-35eb-418e-a0da-292c8b67b49d');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'ad036486-f2c8-4be1-9c23-36def611da15');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'd109f10f-a9d9-465e-8a09-47df8e9fa1e0');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'd2be0199-66ee-4b0e-a94e-dc1611df8177');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '4e5197d9-b8c8-4931-8c00-bef26f35a6b6');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '7dd2d24e-4c4a-4ec8-9fab-33064141dbda');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '3bddb143-125c-4e04-b0a7-099f456b1472');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'eb2f2864-0eaa-408a-9577-2989ad49d147');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '5303b8d1-6c1a-423b-a2c3-d928350e3d11');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'bb138143-13a0-4b6e-ae32-1dbc0a83a576');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '16f5bd13-3bb4-4eab-8a50-bf68a8b78cf0');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '3a70219b-6a08-469c-a405-e02bf1ee2cf2');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '8cea7dd7-75e3-47d7-9589-976de815ec24');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'e424c6af-03a1-4572-bd34-31a547c8df13');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '83e5dfdd-1bc1-481f-8dc2-e3d8884730a2');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '3524304d-c372-4449-8743-562a47903692');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '365a40d4-a193-4a42-b756-1bd97d6ce679');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'f61fdd9d-346b-4bf2-8680-ea4eeee167db');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '4a9e3456-33a2-4615-9b7e-fa6301c6cf17');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'd4dbad47-4e7f-448e-be7b-ec461a4f2f5d');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '39cad863-d669-4cad-9d48-ef281329d233');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '1fbe1c95-d916-4676-9514-e8e95ca7dd78');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '0afd7191-46da-42c5-ab2e-33757a7dec37');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'a73ff6e6-cab0-4829-85b5-5e98c11ce7ae');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '4841d455-7b84-47ed-a3d2-93d5e42d407c');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '70b7b4d8-8e9d-4c56-85dd-772c06b2fe42');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'd17378c1-5046-4360-99ee-75182a26e5ec');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '09c86466-821a-44b2-9210-36a618d08a78');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '0fb693d4-66d7-4633-9d09-1473c3038f6e');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '05e3d800-057d-497a-8916-e406dae5cfea');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '07ae0908-da25-43cf-b1f1-82c3123b1ebe');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '8822a91d-d5e3-415e-b245-3725b3598b79');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'be178bf7-c03b-48d8-9602-05b906ea6cba');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '648bd9e4-f161-4b86-9aaa-46a9486d5acf');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'ae6c4361-2f5f-4133-80bb-a7c1fcb70588');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'ef5e5203-97df-468d-bfa0-2a3d64f4c1ca');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'c939f87d-6cd9-405a-9e7f-8b74ae1e2797');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '7604d919-b3dc-491f-bf9c-89d6657e7cd1');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '5894bde9-4f8b-48d7-871f-94e3d4e9641b');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'a02c92e7-45c0-4543-abbb-3d20ca466f41');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'df2e0873-6539-47e8-9c4d-61c342204336');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '34dde886-3bee-402f-8f99-652d14634800');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '7c38698d-7db3-48e5-882f-76aee3bfd999');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '1788419b-6f18-4467-808f-a73627806cb5');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '2e93a69c-6e21-41d7-9c9a-2031f7d7dbe6');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'fb9a8a15-1b74-4c7c-93de-d096d99c9e3c');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '2da8dcb7-d0ed-41a0-bb38-ce78e8556e83');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '8a98ac0b-b89c-42df-9358-0440c264d2fc');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '05315d10-2e09-4b44-bfb9-826358b298e0');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '0bb76b9a-0072-438d-83ed-a08822c36b1d');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '5ffbe027-28cc-4772-bc7d-b0eb580e38f7');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'f70cb395-36ee-45eb-9c24-863dde4390e8');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '6a3648ce-5e62-457d-926f-1b46e7d9da46');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'f7d3fef4-7fb6-4e13-8c2d-8c433e353743');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '726e905f-253f-4e58-bc3d-828df2ae5fbc');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '5d0f52db-3b7f-4431-9d2a-bed455939904');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '1d67e36f-5164-44ef-b476-f6954c707563');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '7f149e82-5599-46e6-ad99-853bdf52c729');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '1044f952-b753-45bf-8f18-a7cca16e6cc0');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '9036b668-0295-4d9d-9117-8418e939e36f');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'c2602244-50d1-43f0-b2a5-5929baa487e0');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '046970d6-f118-49bd-92b0-382f407f9cc8');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '792e259e-713e-4f1a-9bd5-1b84c3567ff9');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '32b50225-0657-4de3-ae51-959f1de68282');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '1bc893b2-5227-4cd2-871d-10cdf3b89da4');
INSERT INTO "public"."product_category" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', '00e865af-c686-404a-8760-dbb3bca5ecbc');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '0b250eab-a67a-4d50-bdfc-2750efcd6142');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '3c9af24e-e571-431a-bd5b-00f1d79b07cc');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '48744cc6-48df-48b4-9539-f8699185a13a');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'b1bcf436-aa43-41a7-9c22-79b2f990efff');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'd93ed170-8f13-4e14-830c-4e616a23c355');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '0781d07f-d69f-4149-8288-07d79041e0f1');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '8e26b1a7-8d3a-4f57-b14c-07558036ae6c');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '7d18cc78-50b1-457f-a588-2694473582b1');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'b9f93620-7790-429d-9c94-25107f7d196c');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'a2f37ca8-e1b1-4969-abb1-2af26e9ffc62');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'e61707f0-a0ae-4662-a3b6-3e5354e0587f');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '82300a7e-38a5-4ca7-9998-2b14812abf0c');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'b7aeb673-102c-41d5-94f3-f2d05e0d4c81');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '60904db1-acc7-47ea-88eb-bbbe9db46162');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '16264aae-052d-4479-be0c-fc0b2ef169aa');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'd8733286-c141-496c-8b55-0ef2710accd5');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'f719f82c-39b4-4a61-8884-058aebea1c7f');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'e2041c77-4380-4b2a-93a6-f4dcf3ceb3b6');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'd8b08a2b-d034-4131-acb3-477277c6d82a');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'cad2a041-6eaf-4f39-bef4-2ade3a55d77d');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'b29c845c-07de-408d-94bf-fb682c9921f8');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'd739d9ce-3361-40f8-a0ca-c6e45af0b40f');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'd5ff8b3b-ed80-484c-9d5f-12cf5273c94e');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '846e749f-781f-4aff-8eff-0426b20d0de8');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '9e968995-d903-42c7-aaab-0f68a0c9d920');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'f10b711e-742f-404d-813f-0c2ca8542ff2');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'caf67522-2aed-4394-ad89-1d7ffc447518');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '59ccefa3-b1f3-4b0b-9587-e428ba6a205d');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '05ab7b51-b250-4bbd-9cd2-bb39baf5842e');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '8e75b808-6952-465c-88a9-a5babf0f14c3');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '38d52275-417b-4327-86dc-22fad45e0301');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '7b1b08fb-b5ba-4280-9e80-afb2ce9e439a');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'af046d5b-65f2-4cef-99c3-b0723c142b50');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '2dba15fb-c40b-471b-8192-40552834bc90');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '226f6a96-b492-442f-9a26-f3b6698a5653');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'ef4056e2-0c63-4f44-8f64-bf4a9b66d56d');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'cb55c3b8-a243-4e26-8e7c-9f446faf9fe8');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'd8d198c2-c5fd-484e-a4d2-d0e83c5c034d');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '196c8399-4eb7-47dc-9db1-2cf06527f24c');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '5597ec2d-7c51-4ed7-ad2b-484275f0a0c0');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '0c448a28-1e50-4854-866b-f046e22d0d58');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'c532521d-7228-43ba-a95a-57c0cc2fd1d5');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '4c88f233-12d9-4718-b52e-9bedbe5685fb');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '2b39d691-793e-47d9-ae37-adb468fd7d1c');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'd7f3591b-59d4-41d3-a9d8-b21120718307');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '95875f70-2d10-47f4-8aa5-b43e8ee7eeae');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '6c14399d-4d4d-4eb9-8f9e-0ed36241dce8');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'f6867f3e-5cba-4721-a8d0-17d1a82332ca');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'eeee67a5-15b8-4c5e-914f-a4b7b7a8160e');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'bf42e9fa-ccaa-4255-9c14-ca52919dfe13');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '7f438404-11b4-493d-b26d-fc68b64c4beb');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '45969b85-fb2b-479a-93d5-2e97f3e28db5');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'ae9c84d4-2d44-4987-9695-69f81dba90de');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'f38e7690-4f9c-4aea-b82d-55697e4c342b');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'a946fd9d-44a9-4ca8-b197-86d0fb3f99c3');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '0611edfb-ec07-46ed-ae49-7b17caba9826');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'ff51bf02-6f4b-4337-ba76-b5c034ad616e');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '6c858d52-05f1-4629-bcc9-461594625ea0');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '3ffb427b-f473-40bf-9ece-3f4e927bb217');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '0243e37b-9373-40e0-b9ac-82f5bd79d01e');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'd7e4bb4b-e20d-4312-9350-065ebda9dc6a');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '906adfdf-8b62-48bc-8c3d-80e0dd3fc70f');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '7f0a0b8e-70ed-4600-bac5-7ad280ac6191');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '96cd6df4-9e77-4b0c-b0db-5d2f8b9c9fea');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '5aa94d1c-036f-44c0-a173-9a8683634f44');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '10a0646e-d445-44c0-bbeb-98b257b9de1e');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '0727c619-f8e7-407b-a290-e3cf6a8ef673');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '3142edbc-3764-476f-b03b-28511018ddc8');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '87276629-459e-430f-833f-ed4112f15fa5');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '7a14b046-e837-4219-b2c8-e3ced0e147d0');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'b5eca328-9a1a-4164-9441-a8dbcd16cd94');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'a8008b40-cb3c-497a-baec-394c4fe102a4');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '6e290f22-b73e-481e-bc4d-50b6a212c515');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '015be9b3-a974-44dd-92c3-341e71b8a0c8');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '8ee2997b-2ce5-40b7-a116-5e420ae3391b');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '9098463d-e301-426e-9519-adbe7540adb9');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '5011327d-fdb3-4e9e-ba67-340e39307160');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'f3857cd3-cfac-4127-add2-11be4fbddbed');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '3efb29e7-2d0c-4a99-9c0e-02f804586afd');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'b2532dc7-306d-436c-85ea-920f2becd4e5');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'e436becc-4632-4c9b-865b-e52eeaa4d823');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'b388fe53-5dd0-4a86-b99c-c4c5533637d3');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '4db72b73-948b-4748-afc9-595fa95dc3f1');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '4f5348d7-4cc5-45bf-b2fc-b11c0aca9905');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'a80a2ae9-814d-4577-8f23-ea959c891462');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'b2f1bb92-99c6-43b6-97ef-20dca3f4165d');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '616bd56e-606f-4c49-9e51-491fd6f2bb65');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '50696737-a64a-4761-94b6-c3224dabd486');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '1b0946ee-35c6-470f-b72e-817d02091bcd');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'd93f22af-8151-4358-8dff-264b123fa6be');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '6bc7b47e-4179-4cf2-a5bb-c4ea090ef297');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '62ce3ff8-fe78-4775-80c4-9ab23844def4');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '10df813e-1b02-49d5-8389-0915c992c53c');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'c5f96dac-d07a-4a7f-91ad-28e06c216215');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '4aeb9171-2dce-486e-b586-9f7536c8e889');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'f39d7472-164b-4860-b4c7-51e0b00684cb');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '8093514d-3e58-45cc-812f-1c4b04f9c904');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'f7ff8396-f88d-49db-b1f2-dc6fad6fe96f');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '2445fe19-b637-4d6c-898d-4824651278f6');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'a10e684e-553f-4200-9f07-311dbead4a88');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '2ffc2508-b703-4831-9c0b-f96b5c5539dd');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '4d78477c-c274-42c5-8838-9d9a8cb206e2');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'ba8caffe-dd48-4fe2-9cc8-3a9a3abfdd5a');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '7be43317-35eb-418e-a0da-292c8b67b49d');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'ad036486-f2c8-4be1-9c23-36def611da15');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'd109f10f-a9d9-465e-8a09-47df8e9fa1e0');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'd2be0199-66ee-4b0e-a94e-dc1611df8177');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '4e5197d9-b8c8-4931-8c00-bef26f35a6b6');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '7dd2d24e-4c4a-4ec8-9fab-33064141dbda');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '3bddb143-125c-4e04-b0a7-099f456b1472');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'eb2f2864-0eaa-408a-9577-2989ad49d147');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '5303b8d1-6c1a-423b-a2c3-d928350e3d11');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'bb138143-13a0-4b6e-ae32-1dbc0a83a576');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '16f5bd13-3bb4-4eab-8a50-bf68a8b78cf0');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '3a70219b-6a08-469c-a405-e02bf1ee2cf2');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '8cea7dd7-75e3-47d7-9589-976de815ec24');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'e424c6af-03a1-4572-bd34-31a547c8df13');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '83e5dfdd-1bc1-481f-8dc2-e3d8884730a2');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '3524304d-c372-4449-8743-562a47903692');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '365a40d4-a193-4a42-b756-1bd97d6ce679');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'f61fdd9d-346b-4bf2-8680-ea4eeee167db');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '4a9e3456-33a2-4615-9b7e-fa6301c6cf17');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'd4dbad47-4e7f-448e-be7b-ec461a4f2f5d');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '39cad863-d669-4cad-9d48-ef281329d233');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '1fbe1c95-d916-4676-9514-e8e95ca7dd78');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '0afd7191-46da-42c5-ab2e-33757a7dec37');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'a73ff6e6-cab0-4829-85b5-5e98c11ce7ae');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '4841d455-7b84-47ed-a3d2-93d5e42d407c');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '70b7b4d8-8e9d-4c56-85dd-772c06b2fe42');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'd17378c1-5046-4360-99ee-75182a26e5ec');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '09c86466-821a-44b2-9210-36a618d08a78');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '0fb693d4-66d7-4633-9d09-1473c3038f6e');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '05e3d800-057d-497a-8916-e406dae5cfea');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '07ae0908-da25-43cf-b1f1-82c3123b1ebe');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '8822a91d-d5e3-415e-b245-3725b3598b79');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'be178bf7-c03b-48d8-9602-05b906ea6cba');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '648bd9e4-f161-4b86-9aaa-46a9486d5acf');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'ae6c4361-2f5f-4133-80bb-a7c1fcb70588');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'ef5e5203-97df-468d-bfa0-2a3d64f4c1ca');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'c939f87d-6cd9-405a-9e7f-8b74ae1e2797');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '7604d919-b3dc-491f-bf9c-89d6657e7cd1');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '5894bde9-4f8b-48d7-871f-94e3d4e9641b');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'a02c92e7-45c0-4543-abbb-3d20ca466f41');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'df2e0873-6539-47e8-9c4d-61c342204336');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '34dde886-3bee-402f-8f99-652d14634800');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '7c38698d-7db3-48e5-882f-76aee3bfd999');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '1788419b-6f18-4467-808f-a73627806cb5');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '2e93a69c-6e21-41d7-9c9a-2031f7d7dbe6');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'fb9a8a15-1b74-4c7c-93de-d096d99c9e3c');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '2da8dcb7-d0ed-41a0-bb38-ce78e8556e83');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '8a98ac0b-b89c-42df-9358-0440c264d2fc');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '05315d10-2e09-4b44-bfb9-826358b298e0');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '0bb76b9a-0072-438d-83ed-a08822c36b1d');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '5ffbe027-28cc-4772-bc7d-b0eb580e38f7');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'f70cb395-36ee-45eb-9c24-863dde4390e8');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '6a3648ce-5e62-457d-926f-1b46e7d9da46');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'f7d3fef4-7fb6-4e13-8c2d-8c433e353743');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '726e905f-253f-4e58-bc3d-828df2ae5fbc');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '5d0f52db-3b7f-4431-9d2a-bed455939904');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '1d67e36f-5164-44ef-b476-f6954c707563');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '7f149e82-5599-46e6-ad99-853bdf52c729');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '1044f952-b753-45bf-8f18-a7cca16e6cc0');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '9036b668-0295-4d9d-9117-8418e939e36f');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'c2602244-50d1-43f0-b2a5-5929baa487e0');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '046970d6-f118-49bd-92b0-382f407f9cc8');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '792e259e-713e-4f1a-9bd5-1b84c3567ff9');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '32b50225-0657-4de3-ae51-959f1de68282');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '1bc893b2-5227-4cd2-871d-10cdf3b89da4');
INSERT INTO "public"."product_category" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', '00e865af-c686-404a-8760-dbb3bca5ecbc');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '0b250eab-a67a-4d50-bdfc-2750efcd6142');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '3c9af24e-e571-431a-bd5b-00f1d79b07cc');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '48744cc6-48df-48b4-9539-f8699185a13a');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'b1bcf436-aa43-41a7-9c22-79b2f990efff');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'd93ed170-8f13-4e14-830c-4e616a23c355');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '0781d07f-d69f-4149-8288-07d79041e0f1');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '8e26b1a7-8d3a-4f57-b14c-07558036ae6c');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '7d18cc78-50b1-457f-a588-2694473582b1');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'b9f93620-7790-429d-9c94-25107f7d196c');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'a2f37ca8-e1b1-4969-abb1-2af26e9ffc62');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'e61707f0-a0ae-4662-a3b6-3e5354e0587f');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '82300a7e-38a5-4ca7-9998-2b14812abf0c');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'b7aeb673-102c-41d5-94f3-f2d05e0d4c81');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '60904db1-acc7-47ea-88eb-bbbe9db46162');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '16264aae-052d-4479-be0c-fc0b2ef169aa');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'd8733286-c141-496c-8b55-0ef2710accd5');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'f719f82c-39b4-4a61-8884-058aebea1c7f');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'e2041c77-4380-4b2a-93a6-f4dcf3ceb3b6');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'd8b08a2b-d034-4131-acb3-477277c6d82a');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'cad2a041-6eaf-4f39-bef4-2ade3a55d77d');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'b29c845c-07de-408d-94bf-fb682c9921f8');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'd739d9ce-3361-40f8-a0ca-c6e45af0b40f');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'd5ff8b3b-ed80-484c-9d5f-12cf5273c94e');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '846e749f-781f-4aff-8eff-0426b20d0de8');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '9e968995-d903-42c7-aaab-0f68a0c9d920');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'f10b711e-742f-404d-813f-0c2ca8542ff2');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'caf67522-2aed-4394-ad89-1d7ffc447518');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '59ccefa3-b1f3-4b0b-9587-e428ba6a205d');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '05ab7b51-b250-4bbd-9cd2-bb39baf5842e');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '8e75b808-6952-465c-88a9-a5babf0f14c3');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '38d52275-417b-4327-86dc-22fad45e0301');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '7b1b08fb-b5ba-4280-9e80-afb2ce9e439a');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'af046d5b-65f2-4cef-99c3-b0723c142b50');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '2dba15fb-c40b-471b-8192-40552834bc90');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '226f6a96-b492-442f-9a26-f3b6698a5653');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'ef4056e2-0c63-4f44-8f64-bf4a9b66d56d');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'cb55c3b8-a243-4e26-8e7c-9f446faf9fe8');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'd8d198c2-c5fd-484e-a4d2-d0e83c5c034d');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '196c8399-4eb7-47dc-9db1-2cf06527f24c');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '5597ec2d-7c51-4ed7-ad2b-484275f0a0c0');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '0c448a28-1e50-4854-866b-f046e22d0d58');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'c532521d-7228-43ba-a95a-57c0cc2fd1d5');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '4c88f233-12d9-4718-b52e-9bedbe5685fb');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '2b39d691-793e-47d9-ae37-adb468fd7d1c');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'd7f3591b-59d4-41d3-a9d8-b21120718307');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '95875f70-2d10-47f4-8aa5-b43e8ee7eeae');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '6c14399d-4d4d-4eb9-8f9e-0ed36241dce8');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'f6867f3e-5cba-4721-a8d0-17d1a82332ca');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'eeee67a5-15b8-4c5e-914f-a4b7b7a8160e');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'bf42e9fa-ccaa-4255-9c14-ca52919dfe13');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '7f438404-11b4-493d-b26d-fc68b64c4beb');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '45969b85-fb2b-479a-93d5-2e97f3e28db5');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'ae9c84d4-2d44-4987-9695-69f81dba90de');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'f38e7690-4f9c-4aea-b82d-55697e4c342b');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'a946fd9d-44a9-4ca8-b197-86d0fb3f99c3');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '0611edfb-ec07-46ed-ae49-7b17caba9826');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'ff51bf02-6f4b-4337-ba76-b5c034ad616e');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '6c858d52-05f1-4629-bcc9-461594625ea0');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '3ffb427b-f473-40bf-9ece-3f4e927bb217');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '0243e37b-9373-40e0-b9ac-82f5bd79d01e');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'd7e4bb4b-e20d-4312-9350-065ebda9dc6a');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '906adfdf-8b62-48bc-8c3d-80e0dd3fc70f');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '7f0a0b8e-70ed-4600-bac5-7ad280ac6191');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '96cd6df4-9e77-4b0c-b0db-5d2f8b9c9fea');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '5aa94d1c-036f-44c0-a173-9a8683634f44');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '10a0646e-d445-44c0-bbeb-98b257b9de1e');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '0727c619-f8e7-407b-a290-e3cf6a8ef673');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '3142edbc-3764-476f-b03b-28511018ddc8');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '87276629-459e-430f-833f-ed4112f15fa5');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '7a14b046-e837-4219-b2c8-e3ced0e147d0');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'b5eca328-9a1a-4164-9441-a8dbcd16cd94');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'a8008b40-cb3c-497a-baec-394c4fe102a4');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '6e290f22-b73e-481e-bc4d-50b6a212c515');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '015be9b3-a974-44dd-92c3-341e71b8a0c8');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '8ee2997b-2ce5-40b7-a116-5e420ae3391b');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '9098463d-e301-426e-9519-adbe7540adb9');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '5011327d-fdb3-4e9e-ba67-340e39307160');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'f3857cd3-cfac-4127-add2-11be4fbddbed');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '3efb29e7-2d0c-4a99-9c0e-02f804586afd');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'b2532dc7-306d-436c-85ea-920f2becd4e5');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'e436becc-4632-4c9b-865b-e52eeaa4d823');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'b388fe53-5dd0-4a86-b99c-c4c5533637d3');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '4db72b73-948b-4748-afc9-595fa95dc3f1');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '4f5348d7-4cc5-45bf-b2fc-b11c0aca9905');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'a80a2ae9-814d-4577-8f23-ea959c891462');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'b2f1bb92-99c6-43b6-97ef-20dca3f4165d');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '616bd56e-606f-4c49-9e51-491fd6f2bb65');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '50696737-a64a-4761-94b6-c3224dabd486');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '1b0946ee-35c6-470f-b72e-817d02091bcd');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'd93f22af-8151-4358-8dff-264b123fa6be');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '6bc7b47e-4179-4cf2-a5bb-c4ea090ef297');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '62ce3ff8-fe78-4775-80c4-9ab23844def4');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '10df813e-1b02-49d5-8389-0915c992c53c');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'c5f96dac-d07a-4a7f-91ad-28e06c216215');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '4aeb9171-2dce-486e-b586-9f7536c8e889');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'f39d7472-164b-4860-b4c7-51e0b00684cb');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '8093514d-3e58-45cc-812f-1c4b04f9c904');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'f7ff8396-f88d-49db-b1f2-dc6fad6fe96f');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '2445fe19-b637-4d6c-898d-4824651278f6');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'a10e684e-553f-4200-9f07-311dbead4a88');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '2ffc2508-b703-4831-9c0b-f96b5c5539dd');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '4d78477c-c274-42c5-8838-9d9a8cb206e2');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'ba8caffe-dd48-4fe2-9cc8-3a9a3abfdd5a');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '7be43317-35eb-418e-a0da-292c8b67b49d');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'ad036486-f2c8-4be1-9c23-36def611da15');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'd109f10f-a9d9-465e-8a09-47df8e9fa1e0');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'd2be0199-66ee-4b0e-a94e-dc1611df8177');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '4e5197d9-b8c8-4931-8c00-bef26f35a6b6');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '7dd2d24e-4c4a-4ec8-9fab-33064141dbda');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '3bddb143-125c-4e04-b0a7-099f456b1472');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'eb2f2864-0eaa-408a-9577-2989ad49d147');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '5303b8d1-6c1a-423b-a2c3-d928350e3d11');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'bb138143-13a0-4b6e-ae32-1dbc0a83a576');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '16f5bd13-3bb4-4eab-8a50-bf68a8b78cf0');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '3a70219b-6a08-469c-a405-e02bf1ee2cf2');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '8cea7dd7-75e3-47d7-9589-976de815ec24');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'e424c6af-03a1-4572-bd34-31a547c8df13');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '83e5dfdd-1bc1-481f-8dc2-e3d8884730a2');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '3524304d-c372-4449-8743-562a47903692');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '365a40d4-a193-4a42-b756-1bd97d6ce679');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'f61fdd9d-346b-4bf2-8680-ea4eeee167db');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '4a9e3456-33a2-4615-9b7e-fa6301c6cf17');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'd4dbad47-4e7f-448e-be7b-ec461a4f2f5d');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '39cad863-d669-4cad-9d48-ef281329d233');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '1fbe1c95-d916-4676-9514-e8e95ca7dd78');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '0afd7191-46da-42c5-ab2e-33757a7dec37');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'a73ff6e6-cab0-4829-85b5-5e98c11ce7ae');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '4841d455-7b84-47ed-a3d2-93d5e42d407c');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '70b7b4d8-8e9d-4c56-85dd-772c06b2fe42');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'd17378c1-5046-4360-99ee-75182a26e5ec');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '09c86466-821a-44b2-9210-36a618d08a78');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '0fb693d4-66d7-4633-9d09-1473c3038f6e');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '05e3d800-057d-497a-8916-e406dae5cfea');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '07ae0908-da25-43cf-b1f1-82c3123b1ebe');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '8822a91d-d5e3-415e-b245-3725b3598b79');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'be178bf7-c03b-48d8-9602-05b906ea6cba');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '648bd9e4-f161-4b86-9aaa-46a9486d5acf');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'ae6c4361-2f5f-4133-80bb-a7c1fcb70588');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'ef5e5203-97df-468d-bfa0-2a3d64f4c1ca');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'c939f87d-6cd9-405a-9e7f-8b74ae1e2797');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '7604d919-b3dc-491f-bf9c-89d6657e7cd1');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '5894bde9-4f8b-48d7-871f-94e3d4e9641b');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'a02c92e7-45c0-4543-abbb-3d20ca466f41');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'df2e0873-6539-47e8-9c4d-61c342204336');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '34dde886-3bee-402f-8f99-652d14634800');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '7c38698d-7db3-48e5-882f-76aee3bfd999');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '1788419b-6f18-4467-808f-a73627806cb5');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '2e93a69c-6e21-41d7-9c9a-2031f7d7dbe6');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'fb9a8a15-1b74-4c7c-93de-d096d99c9e3c');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '2da8dcb7-d0ed-41a0-bb38-ce78e8556e83');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '8a98ac0b-b89c-42df-9358-0440c264d2fc');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '05315d10-2e09-4b44-bfb9-826358b298e0');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '0bb76b9a-0072-438d-83ed-a08822c36b1d');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '5ffbe027-28cc-4772-bc7d-b0eb580e38f7');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'f70cb395-36ee-45eb-9c24-863dde4390e8');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '6a3648ce-5e62-457d-926f-1b46e7d9da46');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'f7d3fef4-7fb6-4e13-8c2d-8c433e353743');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '726e905f-253f-4e58-bc3d-828df2ae5fbc');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '5d0f52db-3b7f-4431-9d2a-bed455939904');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '1d67e36f-5164-44ef-b476-f6954c707563');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '7f149e82-5599-46e6-ad99-853bdf52c729');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '1044f952-b753-45bf-8f18-a7cca16e6cc0');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '9036b668-0295-4d9d-9117-8418e939e36f');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'c2602244-50d1-43f0-b2a5-5929baa487e0');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '046970d6-f118-49bd-92b0-382f407f9cc8');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '792e259e-713e-4f1a-9bd5-1b84c3567ff9');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '32b50225-0657-4de3-ae51-959f1de68282');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '1bc893b2-5227-4cd2-871d-10cdf3b89da4');
INSERT INTO "public"."product_category" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '00e865af-c686-404a-8760-dbb3bca5ecbc');

-- ----------------------------
-- Table structure for product_category_translations
-- ----------------------------
DROP TABLE IF EXISTS "public"."product_category_translations";
CREATE TABLE "public"."product_category_translations" (
  "id" uuid NOT NULL,
  "category_id" uuid NOT NULL,
  "language_code" varchar(10) COLLATE "pg_catalog"."default" NOT NULL,
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default",
  "seo_title" varchar(255) COLLATE "pg_catalog"."default",
  "seo_description" varchar(500) COLLATE "pg_catalog"."default",
  "seo_keywords" varchar(255) COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."product_category_translations"."language_code" IS '语言代码，如en-US, zh-CN';
COMMENT ON COLUMN "public"."product_category_translations"."name" IS '分类名称';
COMMENT ON COLUMN "public"."product_category_translations"."description" IS '分类描述';
COMMENT ON COLUMN "public"."product_category_translations"."seo_title" IS 'SEO标题';
COMMENT ON COLUMN "public"."product_category_translations"."seo_description" IS 'SEO描述';
COMMENT ON COLUMN "public"."product_category_translations"."seo_keywords" IS 'SEO关键词';

-- ----------------------------
-- Records of product_category_translations
-- ----------------------------
INSERT INTO "public"."product_category_translations" VALUES ('3069421d-4a66-45f3-b53f-c46d7522e38f', '0b250eab-a67a-4d50-bdfc-2750efcd6142', 'zh-CN', '珠宝首饰', '探索精美的珠宝首饰系列，包括项链、手链、戒指、耳环等多种饰品，每一件都经过精心设计，展现独特风格与卓越品质，是您表达个性与品味的理想选择。', '珠宝首饰 - 发现精美的珠宝饰品', '探索精美的珠宝首饰系列，包括项链、手链、戒指、耳环等。每一件饰品都经过精心设计，展现独特的风格与品味。我们提供多样化的选择，满足您不同的场合需求，是赠送自己或亲友的完美礼物。', '珠宝首饰, 精美饰品, 项链, 手链, 戒指, 耳环, 时尚配饰, 品质珠宝', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('b8418973-9dd6-4c2c-8009-ac9ccb14c045', '3c9af24e-e571-431a-bd5b-00f1d79b07cc', 'zh-CN', '目录', '珠宝首饰的分类目录，包含手链、项链与吊坠、戒指、耳环等多种类型，方便您根据喜好快速找到心仪的饰品。', '珠宝首饰分类目录 - 浏览各类饰品', '浏览珠宝首饰的完整分类目录，包括手链、项链、戒指、耳环等多种类型。每种类别都经过精心整理，帮助您快速找到符合个人风格的精美饰品，轻松搭配日常装扮或特殊场合穿着。', '珠宝分类, 饰品目录, 手链, 项链, 戒指, 耳环, 脚链, 发簪', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('9e93a468-7ca6-4334-8cb3-a33eb4147baf', '48744cc6-48df-48b4-9539-f8699185a13a', 'zh-CN', '手链', '精选各类手链，从简约到华丽，展现个性与魅力。无论是单珠手链还是复杂编织款式，都能为您的腕间增添风采。', '手链 - 精选各类个性手链', '探索精美的手链系列，从简约单珠到复杂编织，从金属材质到宝石镶嵌。每款手链都精心设计，展现独特风格，为您的腕间增添魅力，是日常搭配或礼物赠送的理想选择。', '手链, 个性手链, 珠宝手链, 编织手链, 宝石手链', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('24024ea0-d423-4055-8154-7906188265f3', 'b1bcf436-aa43-41a7-9c22-79b2f990efff', 'zh-CN', '项链与吊坠', '优雅的项链与吊坠系列，从经典锁骨链到奢华多层次设计，点缀颈部风情，彰显高贵气质。', '项链与吊坠 - 优雅颈部饰品', '发掘精美的项链与吊坠系列，包括经典锁骨链、吊坠项链、多层次设计等。每款作品都精心打造，展现优雅气质，为您的装扮增添亮点，是提升整体风格的必备单品。', '项链, 吊坠, 锁骨链, 珠宝项链, 时尚吊坠', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('87227a81-081d-45bf-a490-b414a2152781', 'd93ed170-8f13-4e14-830c-4e616a23c355', 'zh-CN', '戒指', '独特设计的戒指系列，从简约素圈到华丽宝石镶嵌，展现个性与品味，成为手指间的艺术表达。', '戒指 - 独特设计指间饰品', '探索精美的戒指系列，从简约素圈到华丽宝石镶嵌，从传统款式到前卫设计。每枚戒指都精心制作，展现独特风格，是表达自我、纪念特殊时刻的理想选择。', '戒指, 宝石戒指, 设计师戒指, 婚戒, 时尚指环', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('fc77449a-8cd9-42d4-89c0-b641cbb1cc50', '0781d07f-d69f-4149-8288-07d79041e0f1', 'zh-CN', '耳环', '多样的耳环系列，从精致耳钉到摇曳耳坠，为您的耳畔增添光彩，成为整体造型的点睛之笔。', '耳环 - 精致耳畔装饰', '浏览精美的耳环系列，包括耳钉、耳坠、耳环等多种类型。每款耳环都经过精心设计，展现不同风格，从日常简约到晚宴华丽，为您的耳畔增添光彩，提升整体造型魅力。', '耳环, 耳钉, 耳坠, 珠宝耳环, 时尚耳饰', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('cdd3e062-9f9e-49ab-85ea-39ac3cdacf92', '8e26b1a7-8d3a-4f57-b14c-07558036ae6c', 'zh-CN', '脚链', '优雅的脚链系列，为足部增添精致装饰，展现女性的柔美与性感，是夏季海滩或特殊场合的理想配饰。', '脚链 - 优雅足部装饰', '探索精美的脚链系列，从简约金属链到宝石镶嵌款式。每款脚链都精心设计，展现女性柔美与性感，是夏季海滩漫步或特殊场合的理想配饰，为您的整体造型增添独特魅力。', '脚链, 珠宝脚链, 装饰脚链, 夏季配饰', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('9f2c8955-97ee-4d5f-9c95-20267940f2cf', '7d18cc78-50b1-457f-a588-2694473582b1', 'zh-CN', '发簪', '传统与现代相结合的发簪系列，以精美的工艺和独特的设计，为您的发髻增添古典韵味与时尚感。', '发簪 - 传统与现代的发饰艺术', '欣赏精美的发簪系列，融合传统工艺与现代设计。每支发簪都经过精心制作，展现古典韵味与时尚风格，为您的发髻增添独特魅力，是东方美学与现代审美完美结合的饰品。', '发簪, 传统发饰, 现代发簪, 东方饰品, 发饰', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('deacf879-5307-4d35-a1a3-d784bd01d8bf', 'b9f93620-7790-429d-9c94-25107f7d196c', 'zh-CN', '发梳', '精致的发梳系列，不仅实用且兼具装饰功能，以优雅的设计点缀发间，展现女性的温婉与优雅。', '发梳 - 实用与装饰并存的发间饰品', '探索精美的发梳系列，兼具实用功能与装饰效果。每把发梳都经过精心设计，展现优雅风格，为您的发间增添亮点，是日常造型或特殊场合的理想配饰，展现女性的温婉与优雅气质。', '发梳, 装饰发梳, 女士发饰, 优雅发饰', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('0f261348-5e26-4d98-a61e-c4af8d233ee5', 'a2f37ca8-e1b1-4969-abb1-2af26e9ffc62', 'zh-CN', '胸针', '独特的胸针系列，以创意设计和精美工艺，为您的服装增添艺术气息，成为整体造型的亮点装饰。', '胸针 - 创意服装装饰品', '浏览精美的胸针系列，从简约金属到宝石镶嵌，从传统图案到现代设计。每枚胸针都精心制作，展现独特风格，为您的服装增添艺术气息，是提升整体造型品质的理想配饰。', '胸针, 时尚胸针, 艺术胸针, 服装配饰', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('1fb0640a-6fc2-49dc-a91c-9f26360aff37', 'e61707f0-a0ae-4662-a3b6-3e5354e0587f', 'zh-CN', '探索', '特别策划的珠宝首饰探索系列，根据性别、年龄和特定款式分类，帮助您精准找到心仪的饰品。', '探索珠宝首饰 - 特别系列分类', '进入珠宝首饰的探索系列，根据性别、年龄和特定款式精心分类。无论是女士、男士还是儿童饰品，或是流行的红绳系列，都能帮助您快速找到符合需求的精美饰品，展现个性与风格。', '珠宝探索, 特别系列, 女士饰品, 男士饰品, 儿童饰品', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('37d417d1-80d9-4f45-96ec-25d27c1a1efe', '82300a7e-38a5-4ca7-9998-2b14812abf0c', 'zh-CN', '女士手链', '专为女性设计的手链系列，融合优雅与时尚元素，展现女性的柔美与魅力，是日常搭配或礼物赠送的理想选择。', '女士手链 - 优雅与时尚的腕间饰品', '探索专为女性设计的手链系列，融合优雅与时尚元素。从简约金属到宝石镶嵌，从编织款式到金属链条，每款手链都精心打造，展现女性的柔美与魅力，是提升整体造型的完美配饰。', '女士手链, 女性饰品, 优雅手链, 时尚手链', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('b7f54435-42ab-4f3f-a215-6625bd5c8802', 'b7aeb673-102c-41d5-94f3-f2d05e0d4c81', 'zh-CN', '男士手链', '专为男性打造的手链系列，以简约、大气的设计展现阳刚之气，是彰显个性与品味的腕间装饰。', '男士手链 - 简约大气的腕间装饰', '浏览专为男性设计的手链系列，以简约、大气的设计展现阳刚之气。从皮革编织到金属链条，从素色到镶嵌宝石，每款手链都精心制作，成为彰显个性与品味的理想配饰，适合各种场合佩戴。', '男士手链, 男性饰品, 阳刚手链, 个性手链', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('b30f95d9-3cae-48be-b4ab-e07db39c5b44', '60904db1-acc7-47ea-88eb-bbbe9db46162', 'zh-CN', '儿童手链', '专为儿童设计的手链系列，以安全材质和可爱造型，为小朋友增添天真与活力，是成长纪念的理想礼物。', '儿童手链 - 安全可爱的童趣饰品', '探索专为儿童设计的手链系列，采用安全材质和可爱造型。从卡通形象到彩色珠子，从简约设计到趣味图案，每款手链都精心制作，为小朋友增添天真与活力，是记录成长时刻的理想礼物。', '儿童手链, 安全饰品, 可爱手链, 儿童礼物', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('e66a75e0-1c57-42da-a62f-f465aee613de', '16264aae-052d-4479-be0c-fc0b2ef169aa', 'zh-CN', '红绳手链', '流行的红绳手链系列，融合传统与时尚元素，以简约设计展现独特魅力，是招财纳福、表达祝福的热门饰品。', '红绳手链 - 传统与时尚的祝福饰品', '浏览流行的红绳手链系列，融合传统与时尚元素。从简约单绳到多股编织，从纯色红绳到搭配宝石珠子，每款手链都精心设计，展现独特魅力，是招财纳福、表达祝福的理想配饰。', '红绳手链, 招财饰品, 传统手链, 时尚红绳', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('9e127f0c-868a-4617-a3e5-973246cd76c6', 'd8733286-c141-496c-8b55-0ef2710accd5', 'zh-CN', '红绳腰链', '独特的红绳腰链系列，以精致设计点缀腰部，展现女性的曲线美，为整体造型增添亮点与个性。', '红绳腰链 - 点缀腰部的时尚饰品', '探索独特的红绳腰链系列，以精致设计点缀腰部。从简约红绳到搭配宝石珠子，从传统编织到现代设计，每款腰链都精心制作，展现女性的曲线美，为整体造型增添亮点与个性，是时尚搭配的点睛之笔。', '红绳腰链, 女士腰链, 时尚腰饰, 红绳饰品', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('2fe8aa0d-630c-482d-aacd-b0d99480c5aa', 'f719f82c-39b4-4a61-8884-058aebea1c7f', 'zh-CN', '按宝石', '根据珍贵宝石分类的珠宝首饰系列，从紫水晶到白水晶，每种宝石都蕴含独特能量与美丽光泽，为您的饰品增添特别意义。', '宝石珠宝首饰 - 探索不同宝石的魅力', '浏览根据珍贵宝石分类的珠宝首饰系列，从紫水晶到白水晶，每种宝石都蕴含独特能量与美丽光泽。我们精选优质宝石，精心制作成手链、项链、戒指等饰品，不仅展现时尚美感，更带来宝石的特别寓意，是您表达个性与追求美好的理想选择。', '宝石珠宝, 宝石手链, 宝石项链, 紫水晶, 绿松石, 白水晶', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('2385ad3f-86e9-4f56-affb-e3de2ff35939', 'e2041c77-4380-4b2a-93a6-f4dcf3ceb3b6', 'zh-CN', '紫水晶', '紫水晶珠宝系列，以其迷人的紫色调和温和能量著称，象征平静与灵性，为佩戴者带来宁静与平衡。', '紫水晶珠宝 - 迷人紫色的能量饰品', '探索紫水晶珠宝系列，以其迷人的紫色调和温和能量著称。我们提供紫水晶手链、项链、戒指等多种款式，每件作品都精选优质紫水晶，精心制作而成。紫水晶象征平静与灵性，能为佩戴者带来宁静与平衡，是追求内心平静的理想配饰。', '紫水晶, 紫水晶珠宝, 紫色饰品, 能量宝石', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('eb01afba-1e11-42de-b2cd-9be43ae89eb7', 'd8b08a2b-d034-4131-acb3-477277c6d82a', 'zh-CN', '绿松石', '绿松石珠宝系列，以其独特的蓝绿色和古老文化象征著称，代表幸运与保护，展现异域风情与自然之美。', '绿松石珠宝 - 蓝绿色的幸运保护符', '浏览绿松石珠宝系列，以其独特的蓝绿色和古老文化象征著称。我们提供绿松石手链、项链、戒指等多种款式，每件作品都精选优质绿松石，精心制作而成。绿松石代表幸运与保护，展现异域风情与自然之美，是追求独特风格与文化意义的理想配饰。', '绿松石, 绿松石珠宝, 蓝绿色饰品, 幸运宝石', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('4eb02114-d97a-41ac-84da-677220fb06a7', 'cad2a041-6eaf-4f39-bef4-2ade3a55d77d', 'zh-CN', '粉晶', '粉晶珠宝系列，以其柔和的粉红色调和爱心能量著称，象征爱与温柔，为佩戴者带来情感和谐与浪漫气息。', '粉晶珠宝 - 爱心能量的浪漫饰品', '探索粉晶珠宝系列，以其柔和的粉红色调和爱心能量著称。我们提供粉晶手链、项链、戒指等多种款式，每件作品都精选优质粉晶，精心制作而成。粉晶象征爱与温柔，能为佩戴者带来情感和谐与浪漫气息，是表达爱意与追求温柔的理想配饰。', '粉晶, 粉晶珠宝, 爱心宝石, 浪漫饰品', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('ca3b33e5-d8e1-4f00-8bfc-ccfa5e9e2e61', 'b29c845c-07de-408d-94bf-fb682c9921f8', 'zh-CN', '月光石', '月光石珠宝系列，以其神秘的蓝白色泽和女性能量著称，象征直觉与情绪平衡，为佩戴者带来温柔的力量与内在和谐。', '月光石珠宝 - 神秘光泽的女性能量饰品', '浏览月光石珠宝系列，以其神秘的蓝白色泽和女性能量著称。我们提供月光石手链、项链、戒指等多种款式，每件作品都精选优质月光石，精心制作而成。月光石象征直觉与情绪平衡，能为佩戴者带来温柔的力量与内在和谐，是追求心灵平静与女性魅力的理想配饰。', '月光石, 月光石珠宝, 女性能量, 直觉宝石', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('7cb20dbe-4d01-4413-9e81-7083a06b02a7', 'd739d9ce-3361-40f8-a0ca-c6e45af0b40f', 'zh-CN', '海蓝宝', '海蓝宝珠宝系列，以其清新的蓝绿色和勇敢能量著称，象征勇气与清晰思维，为佩戴者带来自信与决策力。', '海蓝宝珠宝 - 清新蓝色的勇气饰品', '探索海蓝宝珠宝系列，以其清新的蓝绿色和勇敢能量著称。我们提供海蓝宝手链、项链、戒指等多种款式，每件作品都精选优质海蓝宝，精心制作而成。海蓝宝象征勇气与清晰思维，能为佩戴者带来自信与决策力，是追求突破与成长的理想配饰。', '海蓝宝, 海蓝宝珠宝, 勇气宝石, 蓝色饰品', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('37aef89a-ed7b-4521-960e-ab47c0d53a8e', 'd5ff8b3b-ed80-484c-9d5f-12cf5273c94e', 'zh-CN', '翡翠', '翡翠珠宝系列，以其浓郁的绿色和东方文化象征著称，代表繁荣与长寿，展现高贵与典雅气质。', '翡翠珠宝 - 绿色贵族的东方魅力饰品', '浏览翡翠珠宝系列，以其浓郁的绿色和东方文化象征著称。我们提供翡翠手链、项链、戒指等多种款式，每件作品都精选优质翡翠，精心制作而成。翡翠代表繁荣与长寿，展现高贵与典雅气质，是传承东方文化与追求品质生活的理想配饰。', '翡翠, 翡翠珠宝, 东方文化, 绿色宝石', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('8b7b9f6e-654f-4a52-890e-4c73cc719074', '846e749f-781f-4aff-8eff-0426b20d0de8', 'zh-CN', '孔雀石', '孔雀石珠宝系列，以其独特的绿色条纹和保护能量著称，象征智慧与安全，为佩戴者带来守护与积极思维。', '孔雀石珠宝 - 绿色条纹的智慧保护符', '探索孔雀石珠宝系列，以其独特的绿色条纹和保护能量著称。我们提供孔雀石手链、项链、戒指等多种款式，每件作品都精选优质孔雀石，精心制作而成。孔雀石象征智慧与安全，能为佩戴者带来守护与积极思维，是追求身心保护与智慧启迪的理想配饰。', '孔雀石, 孔雀石珠宝, 保护宝石, 智慧饰品', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('a6565958-f9b9-44ea-8a20-a50f9427295f', '9e968995-d903-42c7-aaab-0f68a0c9d920', 'zh-CN', '黄水晶', '黄水晶珠宝系列，以其明亮的黄色调和繁荣能量著称，象征成功与财富，为佩戴者带来积极心态与丰盛吸引。', '黄水晶珠宝 - 明亮黄色的财富能量饰品', '浏览黄水晶珠宝系列，以其明亮的黄色调和繁荣能量著称。我们提供黄水晶手链、项链、戒指等多种款式，每件作品都精选优质黄水晶，精心制作而成。黄水晶象征成功与财富，能为佩戴者带来积极心态与丰盛吸引，是追求事业成就与物质丰裕的理想配饰。', '黄水晶, 黄水晶珠宝, 财富宝石, 成功饰品', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('2499bdc4-46b3-43aa-b678-1bf2359948e4', 'f10b711e-742f-404d-813f-0c2ca8542ff2', 'zh-CN', '拉长石', '拉长石珠宝系列，以其神秘的变彩效应和直觉能量著称，象征神秘与内在探索，为佩戴者带来灵感与保护。', '拉长石珠宝 - 神秘变彩的直觉能量饰品', '探索拉长石珠宝系列，以其神秘的变彩效应和直觉能量著称。我们提供拉长石手链、项链、戒指等多种款式，每件作品都精选优质拉长石，精心制作而成。拉长石象征神秘与内在探索，能为佩戴者带来灵感与保护，是追求灵性成长与直觉启迪的理想配饰。', '拉长石, 拉长石珠宝, 直觉宝石, 神秘饰品', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('7cb91f08-b0cb-40ac-8296-04fe51329169', 'caf67522-2aed-4394-ad89-1d7ffc447518', 'zh-CN', '黑曜石', '黑曜石珠宝系列，以其深邃的黑色和保护能量著称，象征力量与接地，为佩戴者带来安全感与情绪稳定。', '黑曜石珠宝 - 深邃黑色的保护力量饰品', '浏览黑曜石珠宝系列，以其深邃的黑色和保护能量著称。我们提供黑曜石手链、项链、戒指等多种款式，每件作品都精选优质黑曜石，精心制作而成。黑曜石象征力量与接地，能为佩戴者带来安全感与情绪稳定，是面对挑战与寻求内心平静的理想配饰。', '黑曜石, 黑曜石珠宝, 保护宝石, 力量饰品', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('d5436e7d-b5b2-4bb4-9a34-11b4296c429f', '59ccefa3-b1f3-4b0b-9587-e428ba6a205d', 'zh-CN', '石榴石', '石榴石珠宝系列，以其浓郁的红色调和活力能量著称，象征热情与生命力，为佩戴者带来激情与再生力量。', '石榴石珠宝 - 浓郁红色的热情活力饰品', '探索石榴石珠宝系列，以其浓郁的红色调和活力能量著称。我们提供石榴石手链、项链、戒指等多种款式，每件作品都精选优质石榴石，精心制作而成。石榴石象征热情与生命力，能为佩戴者带来激情与再生力量，是追求活力与情感表达的理想配饰。', '石榴石, 石榴石珠宝, 活力宝石, 红色饰品', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('eb9ec301-58ae-498e-98a5-c657757ed883', '05ab7b51-b250-4bbd-9cd2-bb39baf5842e', 'zh-CN', '珍珠', '珍珠珠宝系列，以其优雅的光泽和经典美感著称，象征纯洁与高贵，展现女性的温婉与魅力，是永不过时的珍贵饰品。', '珍珠珠宝 - 典雅光泽的高贵饰品', '浏览珍珠珠宝系列，以其优雅的光泽和经典美感著称。我们提供珍珠手链、项链、戒指、耳环等多种款式，每件作品都精选优质珍珠，精心制作而成。珍珠象征纯洁与高贵，展现女性的温婉与魅力，是永不过时的珍贵饰品，适合各种场合佩戴，彰显优雅气质。', '珍珠, 珍珠珠宝, 高贵饰品, 典雅配饰', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('2a51e734-609c-493d-842d-92100cf290a5', '8e75b808-6952-465c-88a9-a5babf0f14c3', 'zh-CN', '虎眼石', '虎眼石珠宝系列，以其独特的金黄色调和猫眼效应著称，象征信心与勇气，为佩戴者带来力量与清晰视野。', '虎眼石珠宝 - 金黄色调的力量视野饰品', '探索虎眼石珠宝系列，以其独特的金黄色调和猫眼效应著称。我们提供虎眼石手链、项链、戒指等多种款式，每件作品都精选优质虎眼石，精心制作而成。虎眼石象征信心与勇气，能为佩戴者带来力量与清晰视野，是追求自我肯定与突破困境的理想配饰。', '虎眼石, 虎眼石珠宝, 力量宝石, 金黄色饰品', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('f3a6ca2e-df65-4f7c-8668-b6daf8796d87', '38d52275-417b-4327-86dc-22fad45e0301', 'zh-CN', '萤石', '萤石珠宝系列，以其多样的色彩和心灵能量著称，象征平衡与和谐，为佩戴者带来情绪稳定与精神集中。', '萤石珠宝 - 多彩心灵的平衡和谐饰品', '浏览萤石珠宝系列，以其多样的色彩和心灵能量著称。我们提供萤石手链、项链、戒指等多种款式，每件作品都精选优质萤石，精心制作而成。萤石象征平衡与和谐，能为佩戴者带来情绪稳定与精神集中，是追求心灵平静与精神成长的理想配饰。', '萤石, 萤石珠宝, 心灵宝石, 多彩饰品', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('fa984f8f-d88c-4109-b017-4b02d9cf08f7', '7b1b08fb-b5ba-4280-9e80-afb2ce9e439a', 'zh-CN', '玛瑙', '玛瑙珠宝系列，以其独特的纹路和保护能量著称，象征稳定与勇气，为佩戴者带来平衡与耐心。', '玛瑙珠宝 - 独特纹路的稳定保护饰品', '探索玛瑙珠宝系列，以其独特的纹路和保护能量著称。我们提供玛瑙手链、项链、戒指等多种款式，每件作品都精选优质玛瑙，精心制作而成。玛瑙象征稳定与勇气，能为佩戴者带来平衡与耐心，是面对生活挑战与寻求内心平静的理想配饰。', '玛瑙, 玛瑙珠宝, 稳定宝石, 纹路饰品', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('eeaa86f6-9a4b-4ed4-af96-8e3472deee7f', 'af046d5b-65f2-4cef-99c3-b0723c142b50', 'zh-CN', '朱砂', '朱砂珠宝系列，以其鲜艳的红色和守护能量著称，象征平安与吉祥，为佩戴者带来保护与积极气场。', '朱砂珠宝 - 鲜红守护的平安吉祥饰品', '浏览朱砂珠宝系列，以其鲜艳的红色和守护能量著称。我们提供朱砂手链、项链、戒指等多种款式，每件作品都精选优质朱砂，精心制作而成。朱砂象征平安与吉祥，能为佩戴者带来保护与积极气场，是祈求好运与驱邪避灾的理想配饰。', '朱砂, 朱砂珠宝, 平安饰品, 红色宝石', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('3f1d10c1-e178-439a-adb2-052ec3e695db', '2dba15fb-c40b-471b-8192-40552834bc90', 'zh-CN', '绿东陵', '绿东陵珠宝系列，以其清新的绿色和丰盛能量著称，象征成长与机遇，为佩戴者带来积极变化与幸运吸引。', '绿东陵珠宝 - 清新绿色的丰盛机遇饰品', '探索绿东陵珠宝系列，以其清新的绿色和丰盛能量著称。我们提供绿东陵手链、项链、戒指等多种款式，每件作品都精选优质绿东陵，精心制作而成。绿东陵象征成长与机遇，能为佩戴者带来积极变化与幸运吸引，是追求事业发展与生活改善的理想配饰。', '绿东陵, 绿东陵珠宝, 丰盛宝石, 绿色饰品', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('8b654cac-e0b3-413f-ac0c-fa511c82ed6d', '226f6a96-b492-442f-9a26-f3b6698a5653', 'zh-CN', '青金石', '青金石珠宝系列，以其深邃的蓝色和皇家气质著称，象征智慧与真相，为佩戴者带来洞察力与精神启迪。', '青金石珠宝 - 皇家蓝色的智慧真相饰品', '浏览青金石珠宝系列，以其深邃的蓝色和皇家气质著称。我们提供青金石手链、项链、戒指等多种款式，每件作品都精选优质青金石，精心制作而成。青金石象征智慧与真相，能为佩戴者带来洞察力与精神启迪，是追求知识与心灵成长的理想配饰。', '青金石, 青金石珠宝, 智慧宝石, 皇家饰品', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('aa3dce60-042e-49cd-b784-91daf48578fc', 'ef4056e2-0c63-4f44-8f64-bf4a9b66d56d', 'zh-CN', '白水晶', '白水晶珠宝系列，以其纯净的透明度和放大能量著称，象征纯洁与清晰，为佩戴者带来心灵净化与能量提升。', '白水晶珠宝 - 纯净透明的能量提升饰品', '探索白水晶珠宝系列，以其纯净的透明度和放大能量著称。我们提供白水晶手链、项链、戒指等多种款式，每件作品都精选优质白水晶，精心制作而成。白水晶象征纯洁与清晰，能为佩戴者带来心灵净化与能量提升，是追求灵性成长与身心平衡的理想配饰。', '白水晶, 白水晶珠宝, 能量宝石, 纯净饰品', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('a3ff05c2-3c4d-4d9c-bc74-4e0e8cfd6f5a', 'cb55c3b8-a243-4e26-8e7c-9f446faf9fe8', 'zh-CN', '按符号', '根据文化符号分类的珠宝首饰系列，从莲花到大卫之星，每种符号都蕴含深厚的文化意义与精神价值，为您的饰品增添特别内涵。', '符号珠宝首饰 - 探索文化象征的魅力', '浏览根据文化符号分类的珠宝首饰系列，从莲花到大卫之星，每种符号都蕴含深厚的文化意义与精神价值。我们精选多种文化元素，精心制作成手链、项链、戒指等饰品，不仅展现独特设计，更传递符号背后的寓意，是表达信念与追求的理想选择。', '符号珠宝, 文化饰品, 莲花珠宝, 大卫之星, 佛像饰品', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('c5b29d93-4eba-4edb-a936-160f936b7d1b', 'd8d198c2-c5fd-484e-a4d2-d0e83c5c034d', 'zh-CN', '莲花', '莲花符号珠宝系列，象征纯洁与重生，展现优雅绽放的姿态，为佩戴者带来精神启迪与心灵净化。', '莲花珠宝 - 纯洁重生的优雅精神饰品', '探索莲花符号珠宝系列，象征纯洁与重生。我们提供莲花造型的手链、项链、戒指等多种款式，每件作品都精心设计，展现莲花优雅绽放的姿态。莲花珠宝为佩戴者带来精神启迪与心灵净化，是追求内心平静与精神成长的理想配饰，展现东方文化的深厚底蕴。', '莲花珠宝, 莲花饰品, 纯洁象征, 精神珠宝', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('4ceeb09f-9c9b-456f-b8b8-9d0e18d07f19', '196c8399-4eb7-47dc-9db1-2cf06527f24c', 'zh-CN', '佛陀', '佛陀符号珠宝系列，以庄严的佛像传递智慧与慈悲，为佩戴者带来内心的安宁与祝福，展现佛教文化的深邃内涵。', '佛陀珠宝 - 智慧慈悲的佛教精神饰品', '浏览佛陀符号珠宝系列，以庄严的佛像传递智慧与慈悲。我们提供多种佛像造型的手链、项链、吊坠等饰品，每件作品都精心制作，展现佛教文化的深邃内涵。佛陀珠宝为佩戴者带来内心的安宁与祝福，是追求精神寄托与心灵平静的理想配饰，适合冥想与日常佩戴。', '佛陀珠宝, 佛像饰品, 智慧象征, 佛教饰品', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('98041e19-6a84-4f07-a7e7-361d419a9c29', '5597ec2d-7c51-4ed7-ad2b-484275f0a0c0', 'zh-CN', '禅与阴阳', '禅与阴阳符号珠宝系列，融合东方哲学思想，展现平衡与和谐之美，为佩戴者带来心灵平静与内在稳定。', '禅与阴阳珠宝 - 东方哲学的平衡和谐饰品', '探索禅与阴阳符号珠宝系列，融合东方哲学思想。我们提供禅意图案、阴阳符号等设计的手链、项链、戒指等饰品，每件作品都精心打造，展现平衡与和谐之美。禅与阴阳珠宝为佩戴者带来心灵平静与内在稳定，是追求身心平衡与哲学思考的理想配饰，展现东方智慧的独特魅力。', '禅珠宝, 阴阳饰品, 哲学珠宝, 东方文化', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('62f0592d-fcf0-43ff-ba2c-c6483fb796a1', '0c448a28-1e50-4854-866b-f046e22d0d58', 'zh-CN', '象神与大象', '象神与大象符号珠宝系列，象征智慧与成功，去除障碍，为佩戴者带来好运与繁荣，展现印度文化的神秘魅力。', '象神与大象珠宝 - 智慧成功的印度文化饰品', '浏览象神与大象符号珠宝系列，象征智慧与成功，去除障碍。我们提供象神 Ganesh 造型、大象图案等设计的手链、项链、吊坠等饰品，每件作品都精心制作，展现印度文化的神秘魅力。象神与大象珠宝为佩戴者带来好运与繁荣，是祈求智慧与突破障碍的理想配饰，适合追求成功与积极变化的人士。', '象神珠宝, 大象饰品, 印度文化, 智慧象征', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('a00a2354-08b4-498d-8715-1fed959bf42c', 'c532521d-7228-43ba-a95a-57c0cc2fd1d5', 'zh-CN', '六字真言', '六字真言符号珠宝系列，承载佛教祈愿与祝福，展现精神力量，为佩戴者带来心灵保护与内在平静。', '六字真言珠宝 - 佛教祈愿的精神力量饰品', '探索六字真言符号珠宝系列，承载佛教祈愿与祝福。我们提供刻有 ''Om Mani Padme Hum'' 的手链、项链、吊坠等饰品，每件作品都精心制作，展现佛教文化的精神力量。六字真言珠宝为佩戴者带来心灵保护与内在平静，是冥想辅助与精神寄托的理想配饰，适合追求心灵成长与佛教修行的人士。', '六字真言珠宝, 佛教饰品, 精神力量, 佛教祈愿', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('5b5d96d1-08c8-43b8-81fb-bab3d605bee3', '4c88f233-12d9-4718-b52e-9bedbe5685fb', 'zh-CN', '锦鲤', '锦鲤符号珠宝系列，象征好运与坚持，展现逆流而上的精神，为佩戴者带来积极能量与成功吸引。', '锦鲤珠宝 - 好运坚持的积极能量饰品', '浏览锦鲤符号珠宝系列，象征好运与坚持。我们提供锦鲤造型的手链、项链、吊坠等饰品，每件作品都精心设计，展现锦鲤逆流而上的精神。锦鲤珠宝为佩戴者带来积极能量与成功吸引，是追求目标与克服困难的理想配饰，展现东方文化的吉祥寓意。', '锦鲤珠宝, 锦鲤饰品, 好运象征, 成功能量', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('f71fde3f-aa49-49a6-945e-a3789b5b36d7', '2b39d691-793e-47d9-ae37-adb468fd7d1c', 'zh-CN', '貔貅', '貔貅符号珠宝系列，象征招财进宝与辟邪，为佩戴者带来财富吸引与保护，展现中国传统文化的吉祥寓意。', '貔貅珠宝 - 招财进宝的辟邪吉祥饰品', '探索貔貅符号珠宝系列，象征招财进宝与辟邪。我们提供貔貅造型的手链、项链、吊坠等饰品，每件作品都精心制作，展现中国传统文化的吉祥寓意。貔貅珠宝为佩戴者带来财富吸引与保护，是祈求财运亨通与平安顺利的理想配饰，适合商业人士与追求吉祥的人士。', '貔貅珠宝, 貔貅饰品, 招财吉祥, 中国传统文化', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('a20986e4-5e3f-457f-9ae0-fbf8e9f91a14', 'd7f3591b-59d4-41d3-a9d8-b21120718307', 'zh-CN', '中国生肖', '中国生肖符号珠宝系列，以十二生肖为主题，展现个性与命运连接，为佩戴者带来属相守护与文化认同，是传统节日与日常佩戴的理想选择。', '中国生肖珠宝 - 十二生肖的文化守护饰品', '浏览中国生肖符号珠宝系列，以十二生肖为主题。我们提供鼠、牛、虎等生肖造型的手链、项链、吊坠等饰品，每件作品都精心设计，展现个性与命运连接。生肖珠宝为佩戴者带来属相守护与文化认同，是传统节日赠送与日常佩戴的理想选择，展现中国传统文化的独特魅力与属相寓意。', '生肖珠宝, 生肖饰品, 中国传统文化, 十二生肖', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('7cfe1aa6-f281-409f-89f0-a49ac3b32afc', '95875f70-2d10-47f4-8aa5-b43e8ee7eeae', 'zh-CN', '生命之树', '生命之树符号珠宝系列，象征成长与连接，展现自然和谐之美，为佩戴者带来生命力与平衡感，是追求精神成长的理想配饰。', '生命之树珠宝 - 成长连接的自然和谐饰品', '探索生命之树符号珠宝系列，象征成长与连接。我们提供生命之树图案的手链、项链、吊坠等饰品，每件作品都精心制作，展现自然和谐之美。生命之树珠宝为佩戴者带来生命力与平衡感，是追求精神成长与自然连接的理想配饰，展现跨文化的共同价值与生命意义。', '生命之树珠宝, 自然饰品, 成长象征, 和谐寓意', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('8072a2d9-3906-44b5-b918-e22d6ac7c6b2', '6c14399d-4d4d-4eb9-8f9e-0ed36241dce8', 'zh-CN', '法蒂玛之手', '法蒂玛之手符号珠宝系列，象征保护与好运，以开放手掌设计驱散负面能量，为佩戴者带来平安与祝福，展现中东文化的深厚底蕴。', '法蒂玛之手珠宝 - 保护好运的中东文化饰品', '浏览法蒂玛之手符号珠宝系列，象征保护与好运。我们提供法蒂玛之手造型的手链、项链、吊坠等饰品，每件作品都精心设计，展现中东文化的深厚底蕴。法蒂玛之手珠宝以开放手掌设计驱散负面能量，为佩戴者带来平安与祝福，是祈求保护与吸引好运的理想配饰，适合不同文化背景的人士佩戴。', '法蒂玛之手珠宝, 保护饰品, 中东文化, 好运象征', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('f004fda2-0c99-4a13-8140-4dce467cfb54', 'f6867f3e-5cba-4721-a8d0-17d1a82332ca', 'zh-CN', '邪眼', '邪眼符号珠宝系列，象征保护与净化，以蓝色眼睛设计抵御邪恶目光，为佩戴者带来平安与正能量，展现地中海文化的独特魅力。', '邪眼珠宝 - 保护净化的地中海文化饰品', '探索邪眼符号珠宝系列，象征保护与净化。我们提供蓝色眼睛造型的手链、项链、吊坠等饰品，每件作品都精心制作，展现地中海文化的独特魅力。邪眼珠宝以经典设计抵御邪恶目光，为佩戴者带来平安与正能量，是祈求保护与驱邪避灾的理想配饰，流行于多种文化中，寓意深远。', '邪眼珠宝, 保护饰品, 蓝色眼睛, 地中海文化', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('74bf38ef-6a07-4907-8b8d-06d55d4b4ac0', 'eeee67a5-15b8-4c5e-914f-a4b7b7a8160e', 'zh-CN', '大卫之星', '大卫之星符号珠宝系列，象征犹太文化与精神信仰，以六角星设计展现智慧与神圣几何，为佩戴者带来文化认同与精神力量。', '大卫之星珠宝 - 犹太文化的智慧信仰饰品', '浏览大卫之星符号珠宝系列，象征犹太文化与精神信仰。我们提供六角星造型的手链、项链、吊坠等饰品，每件作品都精心设计，展现智慧与神圣几何的完美结合。大卫之星珠宝为佩戴者带来文化认同与精神力量，是犹太文化传承与信仰表达的理想配饰，展现深厚的历史底蕴与宗教意义。', '大卫之星珠宝, 犹太文化, 六角星饰品, 信仰象征', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('60322c63-950b-4250-8e90-a2cc2b213d2a', '32b50225-0657-4de3-ae51-959f1de68282', 'zh-CN', '念珠', '探索精美的Mala念珠系列，包括菩提子、木质、宝石等多种材质的念珠，每一件都经过精心制作，不仅适用于冥想修行，更是展现个人风格的独特配饰。', 'Mala Beads - 精美念珠系列', '探索精美的Mala念珠系列，包括菩提子、木质、宝石等多种材质。这些念珠不仅适用于冥想修行，帮助集中注意力与平衡能量，更是展现个人风格的独特配饰，为您的日常生活增添精神气息与时尚感。', 'Mala念珠, 菩提子念珠, 木质念珠, 宝石念珠, 冥想配饰', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('fa85c4a6-cce2-45b9-ab28-f3da39ba9ee9', 'bf42e9fa-ccaa-4255-9c14-ca52919dfe13', 'zh-CN', '菩提子念珠', '菩提子念珠系列，采用天然菩提子精心制作，展现质朴与灵性之美，是传统冥想与祈福的理想工具，承载深厚的文化意义。', 'Bodhi Seed Malas - 菩提子念珠系列', '探索菩提子念珠系列，采用天然菩提子精心制作。这些念珠展现质朴与灵性之美，是传统冥想与祈福的理想工具。菩提子象征觉悟与精神成长，每颗珠子都经过精细打磨，为您带来独特质感与深厚的文化体验，是冥想修行与日常佩戴的完美结合。', '菩提子念珠, Bodhi Seed Malas, 冥想念珠, 传统祈福', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('a314c116-e9d6-4fca-89b6-dbcb54172ed7', '7f438404-11b4-493d-b26d-fc68b64c4beb', 'zh-CN', '木质念珠', '木质念珠系列，选用优质木材制作，散发自然木质香气，展现温暖质感与大地能量，为冥想带来平静与接地感。', 'Wood Malas - 木质念珠系列', '浏览木质念珠系列，选用优质木材精心制作。这些念珠散发自然木质香气，展现温暖质感与大地能量。木质念珠为冥想带来平静与接地感，帮助您连接自然与内在力量。每串念珠都经过精细打磨，确保舒适握感，是追求自然生活方式与精神平衡的理想配饰。', '木质念珠, Wood Malas, 自然冥想, 木质香气', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('597cf03d-224c-4d83-8fab-18655824651e', '45969b85-fb2b-479a-93d5-2e97f3e28db5', 'zh-CN', '宝石念珠', '宝石念珠系列，镶嵌多种珍贵宝石，融合美丽与能量疗愈特性，为佩戴者带来独特风格与精神平衡，展现个性与灵性魅力。', '宝石念珠系列', '探索宝石念珠系列，镶嵌多种珍贵宝石，如紫水晶、绿松石、石榴石等。这些念珠融合美丽与能量疗愈特性，为佩戴者带来独特风格与精神平衡。每颗宝石都经过精心挑选与打磨，展现独特光泽与能量频率，帮助增强冥想效果、提升情绪状态。宝石念珠不仅是冥想工具，更是展现个性与灵性魅力的时尚配饰，适合各种场合佩戴。', '宝石念珠, Gemstone Malas, 能量疗愈, 宝石饰品', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('578038b6-8b42-4783-9bcc-3678a0eb4385', 'ae9c84d4-2d44-4987-9695-69f81dba90de', 'zh-CN', '手腕念珠', '手腕念珠系列，专为手腕佩戴设计，小巧精致且方便日常使用，将冥想修行融入日常生活，成为表达信仰与风格的便捷配饰。', '手腕念珠系列', '浏览手腕念珠系列，专为手腕佩戴设计。这些念珠小巧精致，方便日常使用，将冥想修行融入日常生活。手腕念珠采用多种材质，包括菩提子、宝石、木材等，展现不同风格与能量。佩戴手腕念珠不仅是一种时尚选择，更是随时提醒自己保持觉知、平衡情绪的精神象征，适合在工作、学习、旅行等各种场合佩戴，为您的生活增添一份宁静与力量。', '手腕念珠, Wrist Malas, 日常冥想, 便捷配饰', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('879e5f81-8df7-4d1d-a248-1873dd36ed0f', 'f38e7690-4f9c-4aea-b82d-55697e4c342b', 'zh-CN', '稀有沉香念珠', '稀有沉香念珠系列，采用珍贵沉香木制作，散发独特木质香气，具有高度灵性价值，为高级冥想与收藏的理想选择，展现奢华与神圣氛围。', '稀有沉香念珠系列', '探索稀有沉香念珠系列，采用珍贵沉香木精心制作。这些念珠散发独特木质香气，具有高度灵性价值，能提升冥想深度与精神连接。沉香木在东方文化中被视为神圣材料，象征高贵与精神升华。每串沉香念珠都经过精细工艺处理，确保香气持久与质感优良。作为高级冥想工具与收藏品，沉香念珠展现奢华与神圣氛围，是追求精神境界与品味生活的理想选择，适合特别场合与日常珍藏。', '沉香念珠, Agarwood Malas, 珍贵木材, 灵性冥想', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('c4af0faa-4f95-4cbb-bc82-6e332e559719', '7f0a0b8e-70ed-4600-bac5-7ad280ac6191', 'zh-CN', '冥想用品', '探索丰富的冥想用品系列，包括冥想练习工具、精神修行辅助品以及创建神圣空间的装饰品，帮助您打造理想的冥想环境，促进内心平静与精神成长。', '冥想用品 - 打造理想冥想环境', '探索丰富的冥想用品系列，包括冥想练习工具、精神修行辅助品以及创建神圣空间的装饰品。我们的产品精心挑选，帮助您打造理想的冥想环境，促进内心平静与精神成长。无论是初学者还是资深修行者，都能找到适合自己的冥想辅助工具，提升冥想体验与效果。', '冥想用品, 冥想工具, 精神修行, 神圣空间', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('e5e4ef9d-f427-49d8-aac2-e7634e92efb6', 'a946fd9d-44a9-4ca8-b197-86d0fb3f99c3', 'zh-CN', '冥想练习', '冥想练习必备工具，包括唱钵、西藏铃铛等多种辅助用品，帮助您集中注意力，进入深度冥想状态，提升修行效果。', '冥想练习工具 - 提升修行效果', '探索冥想练习必备工具系列，包括唱钵、西藏铃铛、拇指琴等多种辅助用品。这些工具通过声音振动帮助您集中注意力，进入深度冥想状态。我们的产品经过精心挑选与测试，确保音质纯净，效果显著，适合各种冥想传统与个人修行方式，是提升冥想体验与效果的理想选择。', '冥想练习, 冥想工具, 唱钵, 西藏铃铛', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('3b25343b-c886-46ac-8e5e-adff3f7d1d83', '0611edfb-ec07-46ed-ae49-7b17caba9826', 'zh-CN', '唱钵', '精选各种尺寸与材质的唱钵，通过振动产生和谐声音，帮助平衡能量，进入深度放松状态，是冥想与声音疗愈的理想工具。', '唱钵 - 声音疗愈与冥想工具', '探索精选唱钵系列，各种尺寸与材质可选。唱钵通过振动产生和谐声音，帮助平衡能量，进入深度放松状态。我们的唱钵经过严格挑选，确保音质纯净，效果显著，适用于冥想、声音疗愈、瑜伽等多种场合，是提升修行体验与身心平衡的理想选择。', '唱钵, 声音疗愈, 冥想工具, 能量平衡', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('74bc649b-23b5-47a5-bdac-857f82ad3ef4', 'ff51bf02-6f4b-4337-ba76-b5c034ad616e', 'zh-CN', '西藏铜铃', '传统西藏铜铃，以清脆声音标志冥想阶段，帮助集中注意力，创造神圣氛围，是藏传佛教修行与个人冥想的珍贵辅助工具。', '西藏铜铃 - 标志冥想阶段的神圣工具', '浏览传统西藏铜铃系列，以清脆声音标志冥想阶段。我们的西藏铜铃采用传统工艺制作，声音纯净悠扬，帮助集中注意力，创造神圣氛围。这些铜铃在藏传佛教修行中具有重要地位，同样适合个人冥想使用，为您的修行带来传统智慧与精神力量，是连接古老文化与现代修行的桥梁。', '西藏铜铃, 冥想标志, 神圣氛围, 佛教修行', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('16648d8c-1724-42e2-9dc4-5677b93a4bbd', '6c858d52-05f1-4629-bcc9-461594625ea0', 'zh-CN', '拇指琴', '便携式拇指琴，以柔和旋律辅助冥想与放松，激发创意，带来愉悦心灵体验，是旅行与日常修行的理想伴侣。', '拇指琴 - 柔和旋律的冥想辅助工具', '探索便携式拇指琴系列，以柔和旋律辅助冥想与放松。我们的拇指琴采用优质材料制作，音色温暖悦耳，激发创意灵感。这种小巧乐器适合旅行与日常修行使用，随时随地为您的心灵带来愉悦体验。无论是冥想前的准备、修行中的辅助，还是放松时刻的陪伴，拇指琴都能帮助您进入平和心境，提升整体修行质量。', '拇指琴, 冥想音乐, 便携乐器, 心灵放松', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('c05cce8f-c1d0-401d-9bbf-dd198b9a5311', '3ffb427b-f473-40bf-9ece-3f4e927bb217', 'zh-CN', '冥想禅园', '微型禅意花园套装，通过布置砂石与小景观创造冥想焦点，培养专注力与耐心，展现日本禅宗美学，为室内空间增添宁静氛围。', '冥想禅园 - 日本禅宗美学的室内冥想工具', '浏览微型禅意花园套装系列，通过布置砂石与小景观创造冥想焦点。我们的禅园套装精心设计，展现日本禅宗美学精髓。这些套装帮助培养专注力与耐心，为室内空间增添宁静氛围。无论是放置在书桌、床头柜还是窗台，禅意花园都能成为您日常冥想的视觉焦点，引导心灵进入平静状态，是连接自然与精神世界的理想桥梁，特别适合城市生活中的心灵避难所创建。', '禅意花园, 禅宗美学, 冥想焦点, 日本文化', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('83c14f5b-72b3-4f92-b295-c75894eece2b', '0243e37b-9373-40e0-b9ac-82f5bd79d01e', 'zh-CN', '冥想坐垫', '精心设计的冥想坐垫，提供舒适支撑，促进正确坐姿，延长冥想时间，采用天然材料制作，展现简约风格，是打造理想冥想空间的基础用品。', '冥想坐垫 - 舒适支撑的修行基础', '探索冥想坐垫系列，精心设计提供舒适支撑。我们的坐垫采用天然材料如有机棉、亚麻、荞麦壳等制作，确保透气性与耐用性。坐垫高度适中，帮助保持脊柱自然曲线，促进正确坐姿，延长冥想时间。简约风格设计融入各种室内装饰，为您的冥想空间增添和谐氛围。无论是传统盘腿坐姿还是椅子辅助冥想，我们都提供适合的坐垫选择，让身体的舒适成为心灵平静的基础。', '冥想坐垫, 舒适支撑, 正确坐姿, 禅修用品', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('d736d760-7c89-4bd8-a81a-c84ffd629f2c', 'd7e4bb4b-e20d-4312-9350-065ebda9dc6a', 'zh-CN', '舌鼓', '疗愈舌鼓，通过低频振动与和谐音阶创造沉浸式声音体验，帮助深度放松，释放压力，是声音疗愈与团体冥想的理想乐器。', '舌鼓 - 低频振动的深度放松乐器', '浏览疗愈舌鼓系列，通过低频振动与和谐音阶创造沉浸式声音体验。我们的舌鼓采用优质钢材制作，音色深沉悠扬，帮助深度放松，释放累积压力。这种现代乐器结合古老声音疗愈原理，适合个人冥想、团体修行以及声音疗愈师使用。舌鼓的简单演奏方式与强大疗愈效果使其成为初学者与专业人士的理想选择，为您的修行带来全新维度的声音能量体验。', '舌鼓, 声音疗愈, 低频振动, 团体冥想', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('c54d0a49-b68f-48e1-9adb-7168df4dd183', '906adfdf-8b62-48bc-8c3d-80e0dd3fc70f', 'zh-CN', '精神修行', '精神修行辅助用品，包括香薰炉与香料、精油与疗愈工具、水晶宝石等，帮助净化空间、平衡能量，提升修行效果，展现自然能量的疗愈力量。', '精神修行用品 - 自然能量的疗愈辅助', '探索精神修行辅助用品系列，包括香薰炉与香料、精油与疗愈工具、水晶宝石等。这些产品帮助净化空间、平衡能量，提升修行效果。我们精选全球优质材料，结合传统智慧与现代科学，展现自然能量的疗愈力量。无论是每日修行、特殊仪式还是家居能量维护，都能找到适合的用品，为您的精神旅程增添支持与保护，引导您走向内在平和与整体健康。', '精神修行, 香薰用品, 精油疗愈, 水晶能量', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('08a95247-5ab8-409c-aca1-901310c471a4', '96cd6df4-9e77-4b0c-b0db-5d2f8b9c9fea', 'zh-CN', '香薰炉与香料', '多样化的香薰炉与天然香料组合，通过香气净化空间，提升意识状态，创造适合冥想与修行的氛围，传承古老嗅觉疗愈传统。', '香薰炉与香料 - 净化空间的嗅觉疗愈工具', '探索香薰炉与香料系列，多样化的组合满足不同修行需求。我们的香薰炉采用陶瓷、金属、石材等材质制作，设计精美实用。搭配的天然香料包括沉香、檀香、藏红花等多种传统配方，通过香气净化空间，提升意识状态。燃烧香料产生的烟雾在许多文化中被视为连接物质与精神世界的桥梁，为您的冥想与修行创造理想氛围，传承古老嗅觉疗愈智慧，是每日修行与特殊仪式的必备用品。', '香薰炉, 天然香料, 净化空间, 嗅觉疗愈', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('4168b5e4-d691-4a7a-a40b-4487ce6910c6', '5aa94d1c-036f-44c0-a173-9a8683634f44', 'zh-CN', '精油与疗愈', '精选有机精油与疗愈工具套装，通过芳香疗法缓解身心症状，促进情绪平衡，提升整体健康，结合现代科学与传统智慧的自然疗愈方案。', '精油与疗愈 - 芳香疗法的自然健康方案', '浏览精油与疗愈工具套装系列，精选有机精油与专业工具。我们的精油采用纯植物提取，无添加合成成分，确保疗效与安全性。套装包括精油、扩香器、按摩工具等，通过芳香疗法缓解压力、焦虑、失眠等身心症状，促进情绪平衡。每种精油都附有详细使用指南，结合现代科学研究与传统疗愈智慧，为用户提供沉浸式的自然疗愈体验。无论是自我护理还是专业疗愈师使用，都能找到适合的方案，帮助恢复身心和谐，提升整体健康水平。', '有机精油, 芳香疗法, 情绪平衡, 自然疗愈', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('84f217ea-e8af-43c9-8e8c-10b4bf06104a', '10a0646e-d445-44c0-bbeb-98b257b9de1e', 'zh-CN', '水晶', '各类能量水晶与矿物，根据独特属性辅助不同修行目标，净化负能量，增强直觉，吸引繁荣，是物质与精神连接的桥梁，展现大地能量的多样性。', '水晶 - 大地能量的精神疗愈工具', '探索能量水晶与矿物系列，根据独特属性辅助不同修行目标。我们的水晶种类丰富，包括紫水晶、绿松石、黄水晶等，每种水晶都附有详细能量说明。这些天然矿物通过振动频率与能量场影响，帮助净化负能量、增强直觉、吸引繁荣、促进愈合等多种效果。水晶可放置在冥想空间、随身携带或制作成珠宝佩戴，是物质世界与精神维度连接的桥梁。我们提供原矿石、雕刻品、珠宝等多种形式，满足不同需求，展现大地能量的多样性与疗愈力量，为您的修行增添自然支持。', '能量水晶, 矿物疗愈, 净化能量, 直觉增强', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('a4c25f35-633a-4aa3-a7ac-f1e7908007cd', '0727c619-f8e7-407b-a290-e3cf6a8ef673', 'zh-CN', '冥想瑜伽气功', '结合冥想、瑜伽与气功的辅助用品，包括瑜伽垫、气功课具等，支持身体练习与能量流动，促进身心整合，提升修行深度与效果。', '冥想瑜伽气功用品 - 促进身心整合的练习工具', '探索冥想瑜伽气功辅助用品系列，包括专业瑜伽垫、气功课具、冥想坐垫等。我们的产品设计符合人体工学，采用环保材料制作，确保舒适度与耐用性。这些工具支持身体练习与能量流动，帮助正确对齐身体结构，预防练习损伤，提升冥想、瑜伽、气功的修行深度与效果。我们提供不同厚度、材质、尺寸的选择，适合初学者与专业人士使用。通过整合身体、心灵与能量练习，这些用品成为您整体健康维护与精神成长的理想辅助，引导您走向身心和谐与内在力量的觉醒。', '瑜伽气功, 冥想练习, 身心整合, 能量流动', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('afe59886-3b23-43fa-8269-17064fbbadb9', '3142edbc-3764-476f-b03b-28511018ddc8', 'zh-CN', '衣物', '舒适的冥想与瑜伽服装，采用有机棉、亚麻等天然面料制作，设计简约宽松，支持自由活动，为修行创造无拘无束的穿着体验，展现内在平和的外在表达。', '冥想瑜伽衣物 - 自然舒适的修行穿着', '浏览冥想与瑜伽服装系列，采用有机棉、亚麻、竹纤维等天然面料制作。我们的设计简约宽松，注重细节，确保穿着舒适度与美观性。衣物款式包括宽松上衣、瑜伽裤、冥想袍等，支持自由活动，适合各种修行姿势。自然色调与精细做工展现内在平和的外在表达，使穿着本身成为修行的一部分。我们注重可持续时尚理念，从材料选择到生产过程都遵循环保标准，为您的修行之旅增添责任感与和谐感，让每一次穿着都成为关爱自己与地球的行动。', '冥想服装, 瑜伽服饰, 天然面料, 舒适穿着', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('306f828e-4224-4cd8-84ee-8746f378b3eb', '87276629-459e-430f-833f-ed4112f15fa5', 'zh-CN', '瑜伽辅助工具', '瑜伽练习辅助工具，包括瑜伽砖、伸展带、倒立辅助器等，帮助正确姿势对齐，深化体式练习，适合不同水平练习者，提升瑜伽修行的安全性与效果。', '瑜伽辅助工具 - 提升练习效果的专业用品', '探索瑜伽练习辅助工具系列，包括瑜伽砖、伸展带、倒立辅助器、瑜伽轮等多种产品。这些工具帮助正确姿势对齐，深化体式练习，特别对初学者或有特殊身体状况的练习者提供必要支持。我们的辅助工具采用优质材料制作，设计符合人体工学，确保使用安全与效果显著。通过这些工具的辅助，练习者可以更深入地体验瑜伽体式的益处，预防运动伤害，逐步提升灵活性与力量。我们提供不同材质、尺寸、功能的选择，满足多样化需求，使瑜伽练习更加高效与愉悦，成为您瑜伽旅程中不可或缺的伙伴。', '瑜伽辅助工具, 姿势对齐, 深化体式, 安全练习', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('5c98f412-5ae8-466c-b9af-8e5a8b91a500', '7a14b046-e837-4219-b2c8-e3ced0e147d0', 'zh-CN', '音叉', '专业音叉套装，通过精准振动频率促进能量平衡，用于声音疗愈、脉轮调和与冥想引导，是精确能量工作的理想工具，展现声波的疗愈潜力。', '音叉 - 精准振动的能量疗愈工具', '浏览专业音叉套装系列，通过精准振动频率促进能量平衡。我们的音叉采用高品质材料制作，频率校准精确，包括脉轮音叉、行星音叉、治疗音叉等多种类型。这些工具用于声音疗愈、脉轮调和、冥想引导以及能量工作，通过声波的物理效应影响身体能量场，帮助恢复平衡与和谐。音叉的使用简单有效，适合疗愈师、冥想指导者以及个人修行者使用。每套音叉都附有详细使用指南与频率说明，帮助您充分发挥其疗愈潜力，探索声波能量的神奇作用，为您的修行带来科学依据的能量支持。', '音叉疗愈, 脉轮调和, 声音疗愈, 能量平衡', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('118928c9-611b-45e9-b4cf-c4955629ee9c', 'b5eca328-9a1a-4164-9441-a8dbcd16cd94', 'zh-CN', '减压旋钮', '手持减压旋钮，通过简单旋转动作转移注意力，缓解焦虑与压力，成为日常减压的理想工具，适合各年龄段人群，随时随地恢复平静。', '减压旋钮 - 简单有效的日常减压工具', '探索手持减压旋钮系列，通过简单旋转动作转移注意力。我们的减压旋钮设计精美，采用优质材料制作，确保流畅旋转与持久使用。这些工具帮助缓解焦虑、压力、注意力不集中等问题，特别适合办公室工作者、学生、旅行者等需要随时放松的人群。旋钮的使用无需特殊技巧，只需简单旋转即可启动减压效果，成为日常生活中恢复平静的理想工具。我们提供多种款式与颜色选择，满足不同个性需求，让减压也成为一种时尚与享受，帮助您在忙碌生活中找回内心平衡与稳定。', '减压工具, 焦虑缓解, 注意力转移, 日常放松', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('380025bf-b0cd-416c-8389-a8a90a844a3d', 'a8008b40-cb3c-497a-baec-394c4fe102a4', 'zh-CN', '创建神圣空间', '打造神圣空间的装饰与用品，包括祈祷祭坛物品、佛教法器等，帮助建立专属修行环境，增强精神连接，创造有利于冥想与祈祷的氛围，赋予空间特殊意义与能量。', '神圣空间用品 - 打造专属修行环境', '探索创建神圣空间的装饰与用品系列，包括祈祷祭坛物品、佛教法器等。这些产品帮助建立专属修行环境，增强精神连接，创造有利于冥想与祈祷的氛围。我们的祭坛装饰包括神龛、佛像、蜡烛台、供品盘等多种类型，经过精心设计与制作，展现不同文化与传统的美学价值。佛教法器如金刚杵、佛铃等，承载深厚宗教意义，为修行提供仪式支持。通过布置这些用品，您可以为冥想空间赋予特殊意义与能量，使其成为心灵避难所与精神力量源泉，促进日常修行的深度与效果，连接物质世界与神圣维度。', '神圣空间, 祈祷祭坛, 佛教法器, 精神环境', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('93c81889-d903-4d0c-82b3-5754a7273204', '6e290f22-b73e-481e-bc4d-50b6a212c515', 'zh-CN', '祈祷祭坛物品', '祈祷祭坛装饰与用品，包括神龛、佛像、蜡烛台等，帮助建立个性化修行空间，创造神圣氛围，连接精神传统，增强每日修行的仪式感与专注力。', '祈祷祭坛物品 - 个性化神圣空间的装饰', '浏览祈祷祭坛物品系列，包括精美神龛、佛像、蜡烛台、供品盘、经幡等。这些用品帮助建立个性化修行空间，创造神圣氛围，连接不同精神传统。我们的祭坛装饰品来自全球各地，涵盖佛教、印度教、原始萨满等多种文化元素，经过精心挑选与设计，确保品质与美感。通过布置祭坛，您可以为每日修行创造仪式感与专注力，使其成为连接神圣能量的桥梁。每件物品都附有文化背景说明，帮助您深入了解其象征意义，正确使用以增强修行效果，使您的冥想空间成为充满力量与灵感的神圣场所。', '祭坛装饰, 祈祷用品, 神圣氛围, 仪式感', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('57db4e39-f3ad-490e-b430-03ebd1c85e23', '015be9b3-a974-44dd-92c3-341e71b8a0c8', 'zh-CN', '佛教法器与金刚杵', '佛教传统法器，包括金刚杵、佛铃等，承载宗教仪式功能，辅助修行者专注咒语、调和能量，是藏传佛教修行与仪式的珍贵工具，展现深厚文化传承。', '佛教法器与金刚杵 - 传统修行仪式工具', '探索佛教传统法器系列，包括金刚杵、佛铃、转经筒等珍贵工具。这些法器承载藏传佛教的核心仪式功能，辅助修行者专注咒语、调和能量、开启智慧。我们的法器采用传统工艺制作，选用优质材料如黄铜、红铜、银等，确保音质纯净与使用持久。每件法器都经过僧侣祝福与能量加持，附有详细使用指南与文化背景说明。使用佛教法器不仅能增强修行效果，更是连接古老智慧与传统文化的方式，帮助修行者进入更深层次的精神实践，体验藏传佛教独特的修行方法与精神力量，是佛教修行者的必备圣物，也是对佛教文化感兴趣的探索者的珍贵收藏。', '佛教法器, 金刚杵, 佛铃, 藏传佛教', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('b0724125-1abf-4b48-8a49-00aa03a8b10c', '792e259e-713e-4f1a-9bd5-1b84c3567ff9', 'zh-CN', '热门趋势', '探索当前最受欢迎的珠宝首饰系列，包括蛇年主题、红绳饰品、翡翠珠宝等热门款式，展现最新潮流趋势与文化元素，满足您对时尚与个性的追求。', '热门趋势珠宝 - 探索最新潮流款式', '探索当前最受欢迎的珠宝首饰系列，从蛇年主题饰品到经典红绳款式，从珍贵翡翠到时尚金属系列。我们的热门趋势板块汇集最新潮流元素与文化主题，精心挑选每一件作品，展现独特设计与卓越工艺。无论是追随时尚步伐还是寻找个性表达，这里都能满足您的需求，为您的装扮增添亮点与话题性，成为潮流前沿的理想选择。', '热门珠宝, 趋势饰品, 蛇年主题, 红绳珠宝', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('3016dea5-3164-444e-b464-4c1e39e852e0', '8ee2997b-2ce5-40b7-a116-5e420ae3391b', 'zh-CN', '蛇年2025', '2025蛇年主题珠宝系列，融合传统生肖元素与现代设计，展现灵动与智慧，为生肖年份增添特别纪念意义，成为新年礼物与自我表达的理想选择。', '蛇年2025珠宝 - 生肖主题的灵动设计', '探索2025蛇年主题珠宝系列，融合传统生肖元素与现代设计。每件作品精心打造蛇的灵动形态，采用多种材质如宝石、金属、木材等呈现独特风格。蛇象征智慧、重生与变革，在东方文化中具有深厚意义。这些珠宝不仅是新年的完美礼物，更是佩戴者个性与文化传承的表达。无论是手链、项链还是戒指，都能为您的装扮增添特别的生肖年份纪念意义，展现独特魅力与文化自信，成为新年期间的话题焦点与时尚亮点。', '蛇年珠宝, 生肖饰品, 2025趋势, 智慧象征', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('2a32364a-5eab-422e-beb0-530e72bdfea8', '9098463d-e301-426e-9519-adbe7540adb9', 'zh-CN', '红绳', '流行红绳珠宝系列，以简约设计与文化寓意著称，象征保护与好运，展现东方美学，为日常佩戴带来一抹亮色与积极能量。', '红绳珠宝 - 传统保护的能量饰品', '浏览红绳珠宝系列，以简约设计与文化寓意著称。我们的红绳手链、项链等饰品采用优质红线编织，搭配各种宝石、金属坠饰，展现东方美学精髓。红绳在许多文化中象征保护、好运与积极能量，常用于驱邪避灾、祈求平安。这些珠宝适合日常佩戴，为您的装扮增添一抹亮色，同时传递美好寓意。无论是自用还是赠送亲友，红绳珠宝都是表达祝福与关怀的理想选择，连接传统智慧与现代时尚。', '红绳珠宝, 保护饰品, 东方文化, 好运象征', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('29ada3d9-db5c-4b15-b0cf-6b36c3fb7e09', 'f3857cd3-cfac-4127-add2-11be4fbddbed', 'zh-CN', '翡翠项链', '精选翡翠项链系列，展现宝石的温润光泽与高贵气质，融合传统工艺与现代设计，成为彰显品味与传承文化的理想饰品，适合各种重要场合。', '翡翠项链 - 温润高贵的东方宝石', '探索精选翡翠项链系列，展现宝石的温润光泽与高贵气质。我们提供多种款式，从传统珠串到现代镶嵌设计，每件作品都采用优质翡翠制作，确保颜色纯正与质地细腻。翡翠在东方文化中象征繁荣、长寿与高贵，佩戴翡翠项链不仅是时尚选择，更是文化传承与品味彰显的方式。这些项链适合正式场合、礼品赠送以及日常珍藏，为您的装扮增添优雅气质，成为传递东方美学与个人风格的完美配饰。', '翡翠项链, 东方宝石, 高贵饰品, 传统工艺', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('35454743-57db-49df-9856-37543aa38416', '3efb29e7-2d0c-4a99-9c0e-02f804586afd', 'zh-CN', '翡翠手链', '精美翡翠手链系列，展现宝石的自然纹理与优雅色泽，结合舒适佩戴体验，成为日常搭配与礼物赠送的理想选择，传递美好寓意与文化价值。', '翡翠手链 - 自然纹理的优雅配饰', '浏览精美翡翠手链系列，展现宝石的自然纹理与优雅色泽。我们的手链采用优质翡翠制作，款式多样，包括珠串、镶嵌、雕刻等多种形式。翡翠手链不仅美观大方，还具有良好的佩戴舒适度，适合日常搭配各种风格装扮。在东方文化中，翡翠象征纯洁、平安与和谐，是赠送亲友表达祝福的理想选择。每件作品都经过精心打磨与质量检验，确保光泽持久、结构牢固，成为您珠宝收藏中的经典之选，传递美好寓意与文化价值。', '翡翠手链, 自然宝石, 优雅配饰, 平安象征', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('52968c66-51c2-4370-84b9-c4685f5d5b1e', 'b2532dc7-306d-436c-85ea-920f2becd4e5', 'zh-CN', '佛陀手链', '佛陀形象手链系列，以庄严佛像传递智慧与慈悲，展现宗教文化的深厚底蕴，为佩戴者带来心灵安宁与精神寄托，成为信仰表达与日常佩戴的理想结合。', '佛陀手链 - 智慧慈悲的精神配饰', '探索佛陀手链系列，以庄严佛像传递智慧与慈悲。我们提供多种佛像造型的手链，包括释迦牟尼、观音、弥勒等多种类型，采用金属、宝石、木质等材质精心制作。每尊佛像都经过细致雕刻，展现佛教文化的深厚底蕴。佩戴佛陀手链不仅是信仰表达的方式，更是心灵安宁与精神寄托的象征。这些手链适合日常佩戴、冥想辅助以及特殊场合，帮助您保持内心的平静与专注，连接佛教智慧与现代生活，成为精神修行与时尚风格的完美结合。', '佛陀手链, 佛像饰品, 智慧象征, 精神寄托', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('31e6de94-2ed9-4a58-83d7-5e1bf3c32b6a', 'e436becc-4632-4c9b-865b-e52eeaa4d823', 'zh-CN', '佛陀项链', '精致佛陀项链系列，以佛像吊坠展现宗教艺术之美，融合传统工艺与现代设计，为佩戴者带来精神力量与文化认同，成为表达信仰与个人风格的独特饰品。', '佛陀项链 - 宗教艺术的精神饰品', '浏览精致佛陀项链系列，以佛像吊坠展现宗教艺术之美。我们的项链采用优质材料如纯银、黄金、宝石等制作，佛像造型精美，细节丰富，展现不同佛教传统的艺术风格。每件作品都经过工匠精心打磨，确保质感与光泽。佛陀项链不仅是信仰表达的载体，更是个人风格的独特展现。它们适合日常佩戴、宗教仪式以及礼品赠送，帮助佩戴者连接佛教智慧，获得精神力量。通过佩戴佛像，您可以随时提醒自己实践慈悲与智慧，将宗教文化融入日常生活，成为内外和谐的象征。', '佛陀项链, 宗教饰品, 佛像珠宝, 文化传承', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('25d5bc62-6510-4bee-ba24-c337ee288eb2', 'b388fe53-5dd0-4a86-b99c-c4c5533637d3', 'zh-CN', '龙', '龙主题珠宝系列，展现东方神话的威严与力量，融合传统图案与现代设计，为佩戴者带来勇气与繁荣寓意，成为独特文化表达与时尚声明的理想选择。', '龙珠宝 - 权力与繁荣的东方象征', '探索龙主题珠宝系列，展现东方神话的威严与力量。我们的龙形手链、项链、戒指等饰品采用精细工艺制作，呈现龙的灵动姿态与华丽细节。龙在东方文化中象征权力、繁荣与好运，是皇室与尊贵的代表。这些珠宝融合传统图案与现代设计，适合各种场合佩戴，展现独特文化表达。无论是追求时尚个性还是表达文化自豪感，龙珠宝都能成为引人注目的焦点，传递积极能量与高贵气质。每件作品都经过严格质量控制，确保材质优良与工艺精湛，成为您珠宝收藏中的珍品。', '龙珠宝, 权力象征, 繁荣寓意, 东方神话', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('cf766a5f-ec6d-4921-bca1-a62bcdaef625', '4db72b73-948b-4748-afc9-595fa95dc3f1', 'zh-CN', '手镯', '时尚手镯系列，展现大胆设计与材质多样性，从金属光泽到宝石镶嵌，为腕间增添个性与魅力，成为表达自我风格与场合搭配的理想配饰。', '手镯 - 大胆设计的腕间时尚', '浏览时尚手镯系列，展现大胆设计与材质多样性。我们的手镯包括宽边手镯、细手环、镶嵌宝石手镯等多种款式，采用黄金、白金、玫瑰金、宝石等优质材料制作。手镯设计从简约现代到复古华丽，满足不同个性与场合需求。佩戴手镯能够为您的腕间增添个性与魅力，成为整体造型的点睛之笔。无论是单独佩戴还是多层叠搭，都能展现独特的时尚态度。我们提供多种尺寸与调节方式，确保舒适贴合，让时尚与舒适并存，成为日常穿搭与特殊场合的理想配饰。', '时尚手镯, 腕间配饰, 金属光泽, 宝石镶嵌', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('5b116d56-db08-4563-976e-c7a9986f6f30', '4f5348d7-4cc5-45bf-b2fc-b11c0aca9905', 'zh-CN', '925/999银', '高品质银饰系列，采用纯银材质制作，展现银的纯净光泽与精致工艺，提供多样款式选择，从简约到华丽，满足不同风格需求，是日常佩戴与礼物赠送的理想选择。', '925/999银饰 - 纯净光泽的精致珠宝', '探索高品质银饰系列，采用925纯银或999足银精心制作。我们的银饰包括项链、手链、戒指、耳环等多种类型，设计风格从简约现代到复古民族，满足不同审美需求。银饰以其纯净光泽与亲和力著称，不易引起过敏，适合长期佩戴。每件作品都经过精细打磨与质量检验，确保光泽持久、结构牢固。银饰不仅是时尚选择，更具有投资收藏价值，尤其是限量版与手工制作款式。无论是日常穿搭、特殊场合还是作为礼物，银饰都能展现佩戴者的品味与风格，传递纯洁、真诚的美好寓意，成为珠宝收藏中的重要类别。', '纯银饰品, 高品质银饰, 纯净光泽, 手工制作', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('2d64b2c9-4f33-4ea0-baac-d5a6a49c2268', 'b2f1bb92-99c6-43b6-97ef-20dca3f4165d', 'zh-CN', '999黄金珠宝', '奢华黄金珠宝系列，采用999足金制作，展现黄金的高贵色泽与精湛工艺，融合传统与现代设计，成为财富象征与珍贵礼物的完美结合，适合投资收藏与重要场合佩戴。', '999黄金珠宝 - 贵族色调的投资珍品', '浏览奢华黄金珠宝系列，采用999足金精心制作。我们的黄金珠宝包括项链、手链、戒指、耳环、吊坠等多种类型，设计风格从传统福禄寿到现代简约，满足不同文化背景与时尚需求。黄金以其保值增值特性著称，是财富与地位的象征。每件作品都经过精密铸造与细致打磨，确保黄金纯净度与光泽度。黄金珠宝不仅是珍贵礼物的选择，更是财富传承与投资收藏的理想载体。无论是婚庆喜事、节日馈赠还是个人珍藏，黄金珠宝都能展现佩戴者的尊贵气质，传递永恒的价值与美好祝福，成为家族财富与文化传承的重要象征。', '黄金珠宝, 贵族色调, 投资收藏, 保值增值', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('c0b1d4d3-6d84-430c-b42c-ca8b0e861fd2', '616bd56e-606f-4c49-9e51-491fd6f2bb65', 'zh-CN', '狐狸珠宝', '狐狸主题珠宝系列，以灵动造型展现智慧与神秘，融合宝石镶嵌与金属工艺，成为时尚潮流中的独特单品，吸引追求个性与故事性饰品的佩戴者。', '狐狸珠宝 - 智慧神秘的时尚单品', '探索狐狸主题珠宝系列，以灵动造型展现智慧与神秘。我们的狐狸珠宝包括项链、耳环、手链等多种款式，采用黄金、白金、宝石等优质材料制作。狐狸形象通过精细雕刻与镶嵌工艺呈现，细节丰富，栩栩如生。在许多文化中，狐狸象征智慧、机敏、神秘与魅力，这些特质通过珠宝设计传递给佩戴者。狐狸珠宝适合追求个性表达与时尚潮流的人士，成为引人注目的配饰。无论是日常穿搭还是特殊场合，都能为您的装扮增添独特风格与话题性，展现非凡品味与个性魅力，成为珠宝收藏中的创意之选。', '狐狸饰品, 智慧象征, 神秘魅力, 个性珠宝', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('900be388-f4d4-4875-8ac6-99475f8dff3f', '50696737-a64a-4761-94b6-c3224dabd486', 'zh-CN', '铜手链', '纯铜手链系列，利用铜的自然能量与健康益处，展现复古质感与耐用特性，为佩戴者带来时尚与功能性兼具的腕间装饰，是追求自然疗法与复古风格的理想选择。', '铜手链 - 自然能量的复古健康饰品', '浏览纯铜手链系列，利用铜的自然能量与健康益处。我们的铜手链设计多样，包括编织手链、宽边手镯、镶嵌宝石款式等，展现复古质感与耐用特性。铜在传统医学中被认为具有抗炎、能量平衡等功效，佩戴铜手链成为自然疗法的实践方式。这些手链适合追求健康生活方式与复古风格的人士，为腕间增添独特装饰。铜材经过特殊处理，防止氧化变色，长期佩戴依然保持光泽。无论是单独佩戴还是与其他手链叠搭，铜手链都能展现个性魅力，成为连接自然元素与时尚风格的理想选择，特别适合户外爱好者与健康追求者。', '铜手链, 自然疗法, 复古风格, 健康饰品', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('32208943-c7b5-4a02-b540-35f7b040ad0e', '1b0946ee-35c6-470f-b72e-817d02091bcd', 'zh-CN', '收藏品', '珍贵珠宝收藏品系列，包括限量版设计、古董珠宝与稀有宝石作品，展现卓越工艺与历史价值，为收藏家与鉴赏家提供独特投资与审美体验。', '珠宝收藏品 - 珍贵工艺的历史见证', '探索珍贵珠宝收藏品系列，包括限量版设计、古董珠宝与稀有宝石作品。我们的收藏品来自世界各地的知名设计师、皇家御用珠宝商以及历史拍卖会，每件作品都经过专业鉴定与认证，确保其真实性和历史价值。这些珠宝展现不同历史时期的工艺风格，从文艺复兴到装饰艺术时代，为收藏家与鉴赏家提供独特的审美体验。限量版作品则融合现代设计与传统工艺，数量稀缺，具有高度收藏价值。无论是作为投资、传承还是纯粹欣赏，珠宝收藏品都是珍贵的文化遗产与财富象征，帮助您建立具有个性与深度的收藏系列，传承家族文化与艺术品味。', '珠宝收藏品, 限量版设计, 古董珠宝, 稀有宝石', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('3aae0e46-c557-4e11-97ab-1647fcc12feb', 'd93f22af-8151-4358-8dff-264b123fa6be', 'zh-CN', '十二星座系列', '星座主题珠宝系列，融合天文学元素与个人星象特征，通过宝石色彩与符号设计展现独特个性，为佩戴者带来与生辰相关的神秘连接与时尚表达。', '十二星座珠宝 - 神秘星象的时尚表达', '浏览星座主题珠宝系列，融合天文学元素与个人星象特征。我们的十二星座珠宝包括项链、戒指、耳环等多种类型，每件作品根据星座符号、守护星、幸运石等元素进行设计，采用对应色彩的宝石与金属工艺呈现。佩戴星座珠宝不仅是一种时尚表达，更是一种与生辰星象的神秘连接，展现佩戴者的个性特质与宇宙能量。这些珠宝适合星座爱好者、占星学研究者以及追求个性化配饰的人士，成为话题焦点与情感寄托。无论是自用还是作为生日礼物，星座珠宝都能传递特别的寓意，连接个人命运与宇宙奥秘，展现独特的时尚品味与精神追求。', '星座珠宝, 星象符号, 守护石, 个性配饰', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('c5c7fbad-6132-426d-9dca-3ff5eb0885af', '6bc7b47e-4179-4cf2-a5bb-c4ea090ef297', 'zh-CN', '皮革手链', '时尚皮革手链系列，结合柔软材质与金属装饰，展现随性与酷感风格，为腕间增添不羁魅力，是追求休闲与个性表达的理想配饰，适合多种场合搭配。', '皮革手链 - 随性酷感的个性腕饰', '探索时尚皮革手链系列，结合柔软优质皮革与金属装饰。我们的皮革手链提供多种颜色、宽度与扣环设计，展现随性与酷感风格。皮革材质经过特殊处理，确保耐用性与舒适佩戴体验。金属装饰如吊坠、链条、铆钉等增加细节亮点，提升整体设计感。皮革手链适合追求休闲风格与个性表达的人士，能够为腕间增添不羁魅力。无论是搭配牛仔装、休闲衫还是时尚外套，都能展现独特风格。我们提供男女款式选择，每件作品都经过精细制作，确保质量与质感，成为日常穿搭与个性展示的理想配饰，展现自由不羁的生活态度。', '皮革手链, 酷感配饰, 休闲风格, 个性表达', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('179591d0-af2c-4870-9978-c213745c7ced', '62ce3ff8-fe78-4775-80c4-9ab23844def4', 'zh-CN', '金属系列', '金属主题珠宝系列，突出金属本身的质感与光泽，通过锻造、雕刻等工艺展现力量与现代美感，为佩戴者带来强硬与优雅并存的风格选择，成为前卫时尚与经典设计的代表。', '金属珠宝 - 质感光泽的现代力量', '浏览金属主题珠宝系列，突出金属本身的质感与光泽。我们的金属珠宝包括纯银、黄金、玫瑰金、钛钢等多种材质，通过锻造、雕刻、抛光等工艺展现力量与现代美感。这些珠宝设计从简约几何到复杂雕塑风格，适合追求前卫时尚与经典设计的人士。金属珠宝能够为佩戴者带来强硬与优雅并存的风格，成为整体造型的亮点。每件作品都经过精心制作，确保金属纯度与工艺质量。无论是日常佩戴还是特殊场合，金属珠宝都能展现独特的时尚态度，传递现代审美与个性力量，成为珠宝收藏中的经典与前卫之选，永不过时且引人注目。', '金属珠宝, 质感光泽, 现代设计, 力量美感', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('e2a404b4-7be4-4f5e-832d-8e46b782cdf7', 'c2602244-50d1-43f0-b2a5-5929baa487e0', 'zh-CN', '藏式用品', '探索丰富多样的藏式传统用品，从精美的藏式饰品到神圣的修行工具，每一件都蕴含深厚的文化底蕴与精神价值，带您领略雪域高原的独特魅力。', '藏式用品 - 传统与精神的完美融合', '探索丰富多样的藏式传统用品系列，从精美的藏式饰品到神圣的修行工具，每一件都蕴含深厚的文化底蕴与精神价值。我们的藏式用品经过精心挑选，确保材质优良与工艺精湛，展现雪域高原的独特魅力。无论是用于个人修行、家居装饰还是作为珍贵礼物，这些用品都能为您带来独特的文化体验与精神启迪，连接古老智慧与现代生活，成为您了解藏文化的理想窗口。', '藏式用品, 藏式饰品, 修行工具, 藏文化', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('243bc0f3-c170-428e-8136-a663bc2ba2a8', 'a80a2ae9-814d-4577-8f23-ea959c891462', 'zh-CN', '藏式手链', '精美藏式手链系列，采用传统工艺与天然材料制作，展现独特的民族风格与神秘魅力，成为表达个性与文化认同的理想配饰。', '藏式手链 - 民族风格的神秘魅力', '探索精美藏式手链系列，采用传统工艺与天然材料精心制作。这些手链融合藏族独特设计元素，如多彩珠串、金属雕花、佛像图案等，展现浓郁的民族风格与神秘魅力。每件作品都由经验丰富的工匠手工完成，确保细节精致与品质优良。藏式手链不仅是时尚配饰，更承载着藏族人民的信仰与祝福，适合日常佩戴、文化活动或作为礼物赠送，成为表达个性与文化认同的理想选择，为您的装扮增添独特的异域风情。', '藏式手链, 民族饰品, 传统工艺, 佛像图案', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('0e1ef7c1-fa5f-429b-abff-8ee03365228d', '10df813e-1b02-49d5-8389-0915c992c53c', 'zh-CN', '藏式念珠与项链', '藏式念珠与项链系列，结合宗教元素与时尚设计，用于修行与日常佩戴，展现精神信仰与审美风格的完美融合，是连接内心与文化的桥梁。', '藏式念珠与项链 - 信仰与时尚的结合', '浏览藏式念珠与项链系列，结合宗教元素与时尚设计。我们的念珠采用优质木材、宝石、珊瑚等材料制作，颗数遵循传统如108颗、21颗等，适合修行计数与冥想使用。项链则融合佛像、经文、幸运符等元素，设计风格从传统到现代简约。这些饰品不仅是修行工具，更是时尚配饰，展现佩戴者的精神信仰与审美品味。每件作品都经过僧侣加持与能量赋予，确保其神圣性与文化价值。适合宗教仪式、日常佩戴或作为珍贵礼物，帮助您连接内心平静与藏族文化，成为精神修行与时尚表达的双重象征。', '藏式念珠, 念珠项链, 修行工具, 宗教饰品', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('dc090836-523f-45b7-9c47-07ec3840413b', 'c5f96dac-d07a-4a7f-91ad-28e06c216215', 'zh-CN', '藏式戒指', '独特藏式戒指系列，以大胆设计与象征符号展现个性，采用金属与宝石制作，融合传统工艺与现代审美，成为手指间的文化表达与力量象征。', '藏式戒指 - 大胆设计的文化象征', '探索独特藏式戒指系列，以大胆设计与象征符号展现个性。我们的戒指采用优质金属如银、金、铜等制作，镶嵌宝石、珊瑚、松石等珍贵材料，呈现藏族传统图案如八宝、六字真言、佛像等。每枚戒指都经过精细雕刻与手工打磨，确保佩戴舒适与品质优良。藏式戒指不仅是时尚饰品，更承载着祝福、保护、智慧等象征意义，适合各种场合佩戴，成为手指间的文化表达与力量象征。无论是追求个性风格还是文化传承，这些戒指都能为您的装扮增添独特魅力，传递深厚的精神内涵。', '藏式戒指, 象征符号, 传统图案, 金属宝石', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('e2db1de0-2e41-415f-be17-6dda7bc5ddcc', '4aeb9171-2dce-486e-b586-9f7536c8e889', 'zh-CN', '藏式唱钵', '传统藏式唱钵系列，以青铜合金打造，通过敲击产生和谐振动，用于冥想、疗愈与仪式，帮助平衡能量，创造神圣氛围，是声音疗愈的理想工具。', '藏式唱钵 - 和谐振动的冥想工具', '浏览传统藏式唱钵系列，以青铜合金精心打造。这些唱钵通过敲击或摩擦产生深沉和谐的振动，频率独特，用于冥想、声音疗愈、能量净化等多种修行方式。藏式唱钵在佛教仪式中具有重要地位，帮助修行者集中注意力、平衡身心能量、进入深度冥想状态。我们的唱钵经过严格挑选，确保音质纯净、振动持久。每只唱钵都附带专用木槌与使用指南，适合初学者与专业人士使用。无论是个人修行、疗愈工作坊还是家居能量维护，藏式唱钵都能为您创造神圣氛围，带来身心和谐与内在平静，成为声音疗愈领域的珍贵工具。', '藏式唱钵, 声音疗愈, 冥想工具, 能量平衡', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('8e698d49-734b-4d24-be25-85d0194e1128', 'f39d7472-164b-4860-b4c7-51e0b00684cb', 'zh-CN', '藏式经幡', '彩色藏式经幡系列，印有经文与吉祥图案，随风飘动传播祝福与正能量，用于装饰与祈福，为环境增添神圣氛围与文化美感。', '藏式经幡 - 随风传播的吉祥祝福', '探索彩色藏式经幡系列，印有传统经文与吉祥图案。这些经幡采用优质布料制作，色彩鲜艳持久，图案包括佛教经文、佛像、神兽等，具有祈福、驱邪、传播正能量的寓意。经幡在藏族文化中象征神圣的祈祷，随风飘动时 believed to spread spiritual messages and blessings。我们的经幡提供多种尺寸与长度选择，适合家居装饰、庭院布置、旅行纪念或宗教仪式。悬挂经幡不仅为环境增添神圣氛围与文化美感，更是一种参与藏族精神实践的方式，为生活空间带来和谐与安宁，传递美好的愿望与祝福。', '藏式经幡, 经文图案, 吉祥祝福, 家居装饰', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('7116dc67-b03e-456e-89fc-b337525d1a66', '8093514d-3e58-45cc-812f-1c4b04f9c904', 'zh-CN', '藏式转经筒', '藏式转经筒系列，内藏经文，通过旋转积累功德，用于个人修行与祈福，展现精美的工艺与深厚的宗教意义，是藏传佛教的重要法器。', '藏式转经筒 - 旋转积累功德的法器', '浏览藏式转经筒系列，内藏大量经文，通过旋转积累功德与祈福。我们的转经筒采用优质木材、金属、皮革等材料制作，设计从手持小型到大型庭院装饰多种类型。每个转经筒都经过僧侣加持，确保其宗教意义与灵性价值。在藏传佛教中，转经筒代表佛法的传播与修行的实践，旋转一圈相当于诵读内部所有经文。这些法器适合个人修行、家居装饰、寺庙供奉或作为珍贵礼物。无论是手持念经还是庭院陈设，转经筒都能为您的生活空间带来神圣氛围，成为连接物质世界与精神领域的桥梁，传递无尽的祝福与智慧。', '藏式转经筒, 经文法器, 功德积累, 宗教意义', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('0eb57cf3-1657-45da-81a9-69ad01bb5344', 'f7ff8396-f88d-49db-b1f2-dc6fad6fe96f', 'zh-CN', '藏式铜铃', '传统藏式铜铃系列，以纯铜打造，发出清脆声音用于修行与仪式，象征智慧与慈悲的结合，帮助集中注意力，创造神圣庄严的氛围。', '藏式铜铃 - 清脆声音的修行辅助', '探索传统藏式铜铃系列，以纯铜精心打造。这些铜铃设计精美， often featuring dragon and other auspicious symbols, 发出清脆悠扬的声音，用于冥想、祈祷、仪式等多种修行场合。在藏传佛教中，铜铃象征智慧（空性）与慈悲（方法）的完美结合，帮助修行者集中注意力、净化空间、驱散干扰。我们的铜铃提供多种尺寸与声音选择，适合个人修行、寺庙仪式或家居能量净化。每个铜铃都经过精细调试，确保音质纯净、声音传播远。使用铜铃不仅能增强修行效果，更是连接古老智慧与现代精神实践的方式，为您的修行之旅增添传统力量与文化深度。', '藏式铜铃, 修行辅助, 智慧慈悲, 仪式法器', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('cb670621-4af5-4b06-9f11-23d06017aec6', '2445fe19-b637-4d6c-898d-4824651278f6', 'zh-CN', '唐卡', '传统唐卡绘画系列，以矿物颜料绘制佛像与藏族神话，展现精湛的绘画技艺与深厚的精神内涵，是藏族艺术的珍品，具有收藏与装饰价值。', '唐卡绘画 - 藏族艺术的精神珍品', '浏览传统唐卡绘画系列，以矿物颜料精心绘制佛像与藏族神话场景。我们的唐卡由经验丰富的画师手工制作，遵循千年传统工艺，使用金箔、银箔、宝石粉末等珍贵材料，确保色彩鲜艳持久、线条细腻流畅。每幅唐卡都蕴含深厚的宗教意义与精神价值，展现佛菩萨的神圣形象与藏族宇宙观。唐卡不仅是艺术品，更是修行辅助工具，帮助观想与冥想。我们提供多种尺寸与题材选择，包括佛像、菩萨、护法、本尊等，适合家居供奉、寺庙装饰或艺术收藏。每幅唐卡都附有详细背景说明与保养指南，帮助您深入了解其文化内涵，珍藏这份来自雪域高原的艺术瑰宝，为生活空间带来神圣氛围与文化深度。', '唐卡绘画, 藏族艺术, 佛像唐卡, 艺术收藏', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('e531e3ba-d4cd-4976-8e0a-55599a390f39', 'a10e684e-553f-4200-9f07-311dbead4a88', 'zh-CN', '藏式天珠', '珍贵藏式天珠系列，采用天然石头与神秘工艺制作，蕴含古老传说与保护能量，展现独特纹理与神秘魅力，是收藏与佩戴的理想选择。', '藏式天珠 - 神秘纹理的保护宝石', '探索珍贵藏式天珠系列，采用天然石头与古老神秘工艺制作。天珠以其独特的纹理、眼数与图案著称， each pattern carrying specific spiritual significance and protective qualities。在藏族文化中，天珠被视为吉祥物，能够驱邪避灾、带来好运、增强能量。我们的天珠经过严格鉴定，确保其 authenticity and quality，提供多种款式如单珠、手串、项链等。天珠适合收藏、佩戴或作为珍贵礼物，其神秘魅力与文化价值使其成为珠宝爱好者与文化探索者的理想选择。每颗天珠都附有详细图案解释与保养说明，帮助您深入理解其内涵，体验古老智慧的现代传承。', '藏式天珠, 保护宝石, 神秘纹理, 文化传承', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('09384039-e8e4-4adc-ab7f-0b289792426a', '2ffc2508-b703-4831-9c0b-f96b5c5539dd', 'zh-CN', '藏式衣物与围巾', '藏式传统衣物与围巾系列，采用厚实面料与鲜艳色彩，展现民族风情，提供保暖与舒适，是体验藏族生活的理想服饰，适合旅行与特殊场合。', '藏式衣物与围巾 - 民族风情的保暖选择', '浏览藏式传统衣物与围巾系列，采用厚实面料如羊毛、牦牛绒、棉布等制作，色彩鲜艳，图案充满民族风情。我们的衣物包括藏袍、衬衫、帽子等多种类型，围巾则提供多种尺寸与佩戴方式，展现藏族独特的审美与文化特色。这些服饰不仅美观大方，更具有出色的保暖性能与舒适度，适合高原气候与各种户外活动。穿着藏式衣物与围巾，您将深入体验藏族生活方式，成为文化传承的一部分。我们的产品适合旅行者、文化活动参与者或寻求独特风格的人士，为日常装扮增添异域魅力，成为连接传统与现代的时尚桥梁。', '藏式衣物, 民族服饰, 保暖围巾, 传统风格', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('99e9a124-7777-4b1c-b911-d8e12f194671', '4d78477c-c274-42c5-8838-9d9a8cb206e2', 'zh-CN', '藏式海螺', '藏式海螺系列，作为佛教重要法器，用于仪式与冥想，其声音象征佛法传播，帮助净化空间，增强修行氛围，展现神圣的文化意义与实用价值。', '藏式海螺 - 法音传播的神圣法器', '探索藏式海螺系列，作为佛教重要的法器之一。这些海螺采用天然大螺精心打磨，开口发出宏亮声音，声音被认为能净化空间、驱散邪恶、传播佛法。在藏传佛教中，海螺象征佛陀的教法传播与胜利之声，常用于宗教仪式、冥想引导与祈祷活动中。我们的海螺提供多种尺寸与装饰选择，包括简单原生态与镶嵌宝石、金属雕刻等华丽款式。每个海螺都附有使用指南与文化背景说明，确保您正确使用其功能与含义。无论是用于个人修行、寺庙仪式还是家居能量净化，藏式海螺都能为您的精神实践增添神圣氛围，成为连接古老智慧与现代修行的珍贵桥梁，传递和平与觉醒的力量。', '藏式海螺, 法器海螺, 净化空间, 佛法传播', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('d6072dd6-6439-4151-9331-b43fa9ca1197', '00e865af-c686-404a-8760-dbb3bca5ecbc', 'zh-CN', '服装', '探索专为冥想、瑜伽和日常穿着设计的舒适服装系列，融合传统元素与现代风格，展现自然美感与文化深度，为您的身心实践和日常生活提供理想着装选择。', '冥想与瑜伽服装 - 传统与现代的融合', '探索专为冥想、瑜伽和日常穿着设计的舒适服装系列。我们的服装融合传统元素与现代风格，采用有机棉、亚麻、竹纤维等天然面料制作，确保透气性与耐用性。每件作品都经过精心设计，展现自然美感与文化深度，帮助您在练习中自由移动，在日常生活中保持舒适与风格。无论是寻找瑜伽服饰、冥想长袍还是日常休闲装，我们的服装系列都能满足您的需求，成为您身心实践和时尚表达的理想选择。', '冥想服装, 瑜伽服饰, 有机棉服装, 文化风格', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('d855b151-35d7-49c6-b5b2-367124cfc6ec', 'ba8caffe-dd48-4fe2-9cc8-3a9a3abfdd5a', 'zh-CN', '女士', '女士专属服装系列，包括冥想、瑜伽、日常穿着等多种款式，展现优雅与舒适，为现代女性提供全方位的穿着选择，彰显自然气质与个性风格。', '女士冥想与瑜伽服装', '女士专属服装系列，专为冥想、瑜伽和日常穿着设计。我们的女士服装采用贴合女性身形的剪裁，使用柔软透气的天然面料，展现优雅与舒适。款式多样，从宽松的冥想长袍到修身的瑜伽裤，从休闲的佛系T恤到优雅的连衣裙，满足不同场合需求。每件作品都融合传统元素与现代设计，彰显自然气质与个性风格，帮助现代女性在繁忙生活中保持内心平静与外在美丽。', '女士冥想服装, 瑜伽裤, 佛系T恤, 休闲连衣裙', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('2d0c9367-52cf-4069-8ca2-d3669b5554d4', '7be43317-35eb-418e-a0da-292c8b67b49d', 'zh-CN', '冥想瑜伽服', '专为女士设计的冥想瑜伽服装，采用宽松剪裁与柔软面料，确保舒适与自由移动，帮助深度放松与专注练习，展现优雅的修行姿态。', '女士冥想瑜伽服 - 舒适与优雅的修行选择', '专为女士设计的冥想瑜伽服装系列，采用宽松剪裁与柔软面料制作。我们的服装确保舒适与自由移动，帮助您在练习中深度放松与专注。面料采用有机棉、竹纤维等天然材料，透气吸汗，适合各种瑜伽、冥想、气功练习。款式包括宽松长裤、舒适上衣、套装等多种选择，展现优雅的修行姿态。每件作品都经过精心设计，细节考究，为您的练习带来全方位的舒适体验，成为您精神实践的理想着装。', '女士瑜伽服, 冥想服装, 宽松长裤, 舒适上衣', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('9de267ac-5bee-4a7f-b442-c59ccdf3a72d', 'ad036486-f2c8-4be1-9c23-36def611da15', 'zh-CN', '佛系T恤', '女士佛系主题T恤，融合佛教元素与现代设计，采用优质棉料制作，展现精神内涵与时尚风格，成为日常穿着的理想选择，传递平和与智慧。', '女士佛系T恤 - 精神内涵的时尚表达', '女士佛系主题T恤系列，融合佛教元素与现代设计。我们的T恤采用优质棉料制作，亲肤透气，版型修身。图案设计包括佛像、经文、莲花等多种宗教符号，展现精神内涵与艺术美感。这些T恤不仅是日常穿着的理想选择，更是表达个人信仰与追求平和的理想方式。每件作品都经过精心印刷，确保色彩鲜艳持久，图案细节清晰。适合各种场合穿着，为您的日常装扮增添文化深度与时尚风格，成为连接内心与外在的桥梁。', '佛系T恤, 佛教元素, 精神内涵, 日常穿着', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('918a7967-72fd-4d7e-8b87-60b74b5a3a2b', '5011327d-fdb3-4e9e-ba67-340e39307160', 'zh-CN', '上衣', '女士舒适上衣系列，采用柔软面料与精致剪裁，展现女性的柔美与优雅，适合多种场合穿着，成为衣橱中的百搭单品，彰显自然气质。', '女士舒适上衣 - 柔美优雅的日常选择', '女士舒适上衣系列，采用柔软面料与精致剪裁制作。我们的上衣款式多样，包括宽松T恤、修身衬衫、柔软针织衫等，展现女性的柔美与优雅。面料选择注重透气性与舒适度，适合日常穿着、冥想练习或休闲出行。每款上衣都经过精心设计，细节处理考究，能够轻松搭配各种下装，成为衣橱中的百搭单品。无论是追求休闲风格还是优雅气质，都能找到适合的选择，彰显自然气质与个性魅力。', '女士上衣, 舒适面料, 精致剪裁, 百搭配饰', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('99702a4f-250b-4077-9615-079f0a9ab0de', 'd109f10f-a9d9-465e-8a09-47df8e9fa1e0', 'zh-CN', '连衣裙', '女士连衣裙系列，融合传统与现代设计，采用流畅面料制作，展现女性的优雅曲线与文化气质，适合多种场合穿着，成为时尚与舒适的完美结合。', '女士连衣裙 - 优雅曲线的文化表达', '女士连衣裙系列，融合传统与现代设计元素。我们的连衣裙采用柔软流畅的面料制作，剪裁合身，展现女性的优雅曲线。款式包括宽松袍裙、修身包臀裙、层叠半身裙等多种风格，满足不同场合需求。设计细节融入文化元素如佛教图案、藏族色彩、东方美学等，展现独特的文化气质。每条连衣裙都经过精细制作，确保穿着舒适与品质优良。适合参加冥想活动、文化聚会、日常出行等场合，成为时尚与舒适的完美结合，让您在任何场合都能展现优雅与自信。', '女士连衣裙, 优雅曲线, 文化气质, 流畅面料', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('27d9c0c6-57c6-42ed-8335-465771505268', 'd2be0199-66ee-4b0e-a94e-dc1611df8177', 'zh-CN', '外套', '女士外套系列，采用保暖面料与时尚设计，提供多种款式选择，从休闲夹克到优雅大衣，为不同季节与场合提供理想搭配，展现女性的独立与时尚态度。', '女士外套 - 保暖与时尚的完美融合', '女士外套系列，采用高品质保暖面料与时尚设计制作。我们的外套款式多样，包括休闲夹克、连帽外套、修身大衣、皮草外套等，适合不同季节与场合穿着。设计注重细节，如精致刺绣、独特领口、功能性口袋等，展现女性的独立与时尚态度。外套不仅提供出色的保暖性能，更通过精心剪裁与时尚元素提升整体造型。无论是日常通勤、冥想旅行还是社交活动，都能找到理想的搭配，成为您衣橱中的必备单品，为您的装扮增添层次感与风格亮点。', '女士外套, 保暖夹克, 优雅大衣, 时尚设计', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('11b80045-dc09-4179-9301-50f689e055ac', '4e5197d9-b8c8-4931-8c00-bef26f35a6b6', 'zh-CN', '女士长裤', '女士长裤系列，采用舒适面料与修身剪裁，提供多种款式如哈伦裤、直筒裤、阔腿裤等，满足不同风格需求，为日常穿着与冥想练习提供理想选择，展现自然舒适与时尚风格。', '女士长裤 - 舒适与风格的完美结合', '女士长裤系列，采用柔软舒适的面料与修身剪裁制作。我们的长裤款式丰富，包括哈伦裤、直筒裤、阔腿裤、瑜伽裤等，满足不同风格与需求。面料选择注重透气性与弹性，确保穿着舒适，适合日常穿着、冥想练习与各种活动。设计细节如高腰设计、宽松裤脚、精致腰带等，提升整体造型感。每条长裤都经过精细制作，确保版型稳定与品质优良。无论是追求休闲风格、运动装扮还是优雅气质，都能找到理想的款式，成为衣橱中的实用单品，展现自然舒适与时尚风格的完美结合。', '女士长裤, 舒适面料, 修身剪裁, 风格多样', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('3e5ad164-f5a2-4c10-8b3f-35dc56ba25e9', '7dd2d24e-4c4a-4ec8-9fab-33064141dbda', 'zh-CN', '紧身裤', '女士紧身裤系列，采用高弹力面料制作，贴合身形，展现腿部线条，适合瑜伽、健身等运动场合，提供多种颜色与图案选择，成为活力与时尚的运动必备品。', '女士紧身裤 - 贴合身形的运动时尚', '女士紧身裤系列，采用高弹力、透气吸汗的面料制作。我们的紧身裤贴合身形，展现腿部优美线条，提供良好的支撑性与舒适度，适合瑜伽、健身、跑步等多种运动场合。款式包括高腰设计、全长与七分长度、多种颜色与图案选择，满足不同个人风格与运动需求。每条紧身裤都经过压力测试与穿着实验，确保面料耐用、不透光、不起球。设计注重功能性与时尚感的结合，成为运动与时尚的完美融合，帮助您在运动中保持自信与舒适，展现活力四射的形象。', '女士紧身裤, 高弹力面料, 运动时尚, 舒适支撑', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('bdb42281-4505-4360-aa89-227533517ea3', '3bddb143-125c-4e04-b0a7-099f456b1472', 'zh-CN', '哈伦裤', '女士哈伦裤系列，采用宽松裤腿与修身裤腰设计，融合舒适与时尚，展现休闲风格与文化魅力，适合日常穿着与旅行，成为衣橱中的百搭单品。', '女士哈伦裤 - 舒适与时尚的休闲选择', '女士哈伦裤系列，采用宽松裤腿与修身裤腰设计。我们的哈伦裤融合传统与现代元素，展现独特的休闲风格与文化魅力。裤腿宽松部分提供舒适活动空间，而裤腰修身设计确保整体造型不显臃肿。面料选择柔软透气，适合日常穿着、旅行与各种休闲场合。款式包括纯色基本款、民族图案款、刺绣装饰款等多种选择，满足不同搭配需求。哈伦裤能够轻松搭配T恤、衬衫、背心等多种上衣，成为衣橱中的百搭单品，展现随性自在的时尚态度，为您的装扮增添文化深度与个性风格。', '女士哈伦裤, 宽松裤腿, 休闲风格, 文化魅力', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('f154994a-64c4-405b-bb7b-6d0617a703ae', 'eb2f2864-0eaa-408a-9577-2989ad49d147', 'zh-CN', '阔腿裤', '女士阔腿裤系列，采用宽大裤腿设计，展现优雅气质与流畅线条，采用舒适面料制作，适合多种场合穿着，成为时尚与舒适的完美结合，彰显女性的自信与魅力。', '女士阔腿裤 - 优雅气质的时尚单品', '女士阔腿裤系列，采用宽大裤腿设计，展现优雅气质与流畅线条。我们的阔腿裤采用柔软垂坠的面料制作，如亚麻、丝绸、棉质等，确保穿着舒适与品质优良。款式包括高腰设计、腰带装饰、纯色与印花等多种选择，适合不同场合穿着，从正式工作环境到休闲聚会。阔腿裤能够修饰身形，遮盖腿部不完美，同时展现女性的自信与魅力。搭配方式多样，可与简约上衣打造优雅造型，或与时尚外套组合呈现前卫风格，成为衣橱中的时尚主角，引领潮流趋势，为您的装扮增添无限可能。', '女士阔腿裤, 宽大裤腿, 优雅气质, 流畅线条', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('336cfa92-4ca3-47f9-bd58-75263ae2dbb4', '5303b8d1-6c1a-423b-a2c3-d928350e3d11', 'zh-CN', '女士短裤', '女士短裤系列，采用柔软面料与修身设计，提供多种款式选择，从休闲到运动风格，为夏季与日常穿着提供理想选择，展现轻松与活力。', '女士短裤 - 轻松活力的夏季选择', '女士短裤系列，采用柔软透气的面料与修身设计制作。我们的短裤款式多样，包括休闲短裤、运动短裤、热裤等多种风格，满足不同需求。面料选择注重吸汗性与舒适度，适合夏季穿着与各种户外活动。设计细节如弹性腰头、侧边抽绳、时尚口袋等，提升实用与美观性。每条短裤都经过精心剪裁与制作，确保穿着舒适、活动自如。无论是搭配T恤、衬衫还是背心，都能展现轻松与活力，成为夏季衣橱中的必备单品，为您的日常生活增添时尚与便利。', '女士短裤, 舒适面料, 修身设计, 夏季穿着', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('85180bac-35ba-4343-b320-d2249bf0fa04', 'bb138143-13a0-4b6e-ae32-1dbc0a83a576', 'zh-CN', '唐装', '女士唐装系列，融合传统中式元素与现代剪裁，采用精致面料制作，展现东方美学与优雅气质，适合特殊场合与文化活动，成为传统与现代的时尚结合。', '女士唐装 - 传统与现代的优雅融合', '女士唐装系列，融合传统中式元素与现代剪裁设计。我们的唐装采用精致面料如丝绸、提花布、棉麻等制作，展现东方美学的独特魅力。设计细节包括盘扣、立领、云肩、刺绣图案等，展现浓厚的中国文化底蕴。每件唐装都经过精细制作，确保版型合身、质感优良。款式包括唐装外套、连衣裙、旗袍改良款等，适合文化活动、节日庆典、正式场合等穿着。穿着唐装不仅是时尚选择，更是文化传承与审美表达的方式，成为连接传统智慧与现代风格的桥梁，为您的特殊时刻增添优雅与尊贵。', '女士唐装, 传统中式, 东方美学, 文化传承', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('23ff863c-ee50-4e17-9aac-b90555c52d3f', '16f5bd13-3bb4-4eab-8a50-bf68a8b78cf0', 'zh-CN', '两件套', '女士两件套系列，提供多种搭配组合，如上衣与长裤、外套与连衣裙等，展现协调风格与整体造型，为不同场合提供便捷的穿着选择，节省搭配时间。', '女士两件套 - 协调风格的整体造型', '女士两件套系列，提供多种搭配组合，如上衣与长裤、外套与连衣裙、T恤与短裤等。我们的两件套经过精心设计，确保颜色、图案、面料的协调统一，展现整体造型感。每套服装都注重细节，如统一的领口设计、呼应的装饰元素等，提升整体美感。采用舒适面料制作，确保穿着体验优良。适合不同场合，从日常休闲到正式活动，为忙碌的现代女性节省搭配时间，提供便捷的穿着选择。无论是购买整套还是单独搭配其他单品，都能展现时尚品味与个性风格，成为衣橱中的实用之选。', '女士两件套, 整体造型, 协调风格, 节省搭配', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('3e38c3eb-a5ba-4060-bd99-d03bfc36083d', '3a70219b-6a08-469c-a405-e02bf1ee2cf2', 'zh-CN', '连体衣', '女士连体衣系列，采用修身设计与柔软面料，展现女性曲线，提供多种款式选择，从休闲到时尚风格，为日常穿着与特殊场合提供舒适与优雅的着装选择。', '女士连体衣 - 优雅曲线的时尚选择', '女士连体衣系列，采用修身设计与柔软面料制作。我们的连体衣款式多样，包括紧身连体衣、宽松连体裤、吊带连体衣等多种风格，满足不同需求。面料选择注重弹性与透气性，确保穿着舒适与活动自如。设计细节如V领、蝴蝶结、蕾丝装饰等，展现女性优雅曲线与时尚品味。连体衣适合多种场合，从日常休闲到派对出席，提供优雅的着装选择。每件作品都经过精细剪裁与制作，确保版型完美贴合身形，成为衣橱中的时尚亮点，展现女性的独特魅力与自信风采。', '女士连体衣, 修身设计, 柔软面料, 优雅曲线', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('e93ca12b-7164-415e-9d9e-5936f50e761f', '8cea7dd7-75e3-47d7-9589-976de815ec24', 'zh-CN', '运动短裤', '女士运动短裤系列，采用高弹力面料与透气设计，提供良好的支撑性与舒适度，适合各种运动与健身活动，展现活力与时尚，成为运动装扮的理想选择。', '女士运动短裤 - 舒适支撑的活力选择', '女士运动短裤系列，采用高弹力、透气吸汗的面料制作。我们的短裤提供良好的支撑性与舒适度，适合跑步、健身、瑜伽等多种运动场合。款式包括紧身运动短裤、宽松运动短裤、带内衬设计等多种选择，满足不同运动需求。设计注重功能性与时尚感的结合，如反光条纹、时尚图案、修身剪裁等，展现活力与时尚。每条短裤都经过运动测试，确保面料耐用、不透光、不变形。无论是专业训练还是日常锻炼，都能提供理想的穿着体验，帮助您在运动中保持专注与自信，成为运动装扮中的必备单品。', '女士运动短裤, 高弹力面料, 透气设计, 舒适支撑', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('2338f702-15f1-4771-97e9-41b9ce4577b3', 'e424c6af-03a1-4572-bd34-31a547c8df13', 'zh-CN', '藏式服装', '女士藏式服装系列，采用传统藏族元素与工艺，展现独特的民族风格与文化魅力，成为体验藏族文化与表达个性的理想选择，适合文化活动与特殊场合。', '女士藏式服装 - 民族风格的文化表达', '女士藏式服装系列，采用传统藏族元素与精湛工艺制作。我们的服装展现独特的民族风格与文化魅力，如宽松藏袍、彩色珠饰、传统图案等。面料选择厚实保暖的羊毛、棉布、氆氇等，适合高原气候与各种活动。每件作品都经过手工制作，确保细节精致与品质优良。藏式服装不仅是文化活动与节日庆典的理想选择，更是体验藏族生活方式与表达个性的方式。穿着藏式服装，您将深入参与藏族文化传承，成为文化多样性与民族风情的展现者，为特殊场合带来独特的视觉体验与文化深度。', '藏式服装, 民族风格, 文化传承, 传统工艺', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('b12301e3-938d-4df6-a612-89d227178296', '83e5dfdd-1bc1-481f-8dc2-e3d8884730a2', 'zh-CN', '男士', '男士专属服装系列，包括冥想、瑜伽、日常穿着等多种款式，展现简约与舒适，为现代男性提供全方位的穿着选择，彰显自然气质与个性风格。', '男士冥想与瑜伽服装', '男士专属服装系列，专为冥想、瑜伽和日常穿着设计。我们的男士服装采用简约剪裁与舒适面料，展现自然气质与个性风格。款式多样，从宽松的冥想长裤到修身的瑜伽T恤，从休闲外套到传统唐装，满足不同场合需求。每件作品都融合传统元素与现代设计，确保穿着舒适与活动自如，帮助现代男性在繁忙生活中保持内心平静与外在整齐。无论是寻找冥想服饰、瑜伽装备还是日常休闲装，我们的服装系列都能满足您的需求，成为您身心实践和时尚表达的理想选择。', '男士冥想服装, 瑜伽T恤, 休闲外套, 传统唐装', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('aa7e5190-559b-4d41-91b4-40bea5a29bee', '3524304d-c372-4449-8743-562a47903692', 'zh-CN', '冥想瑜伽服', '专为男士设计的冥想瑜伽服装，采用宽松剪裁与柔软面料，确保舒适与自由移动，帮助深度放松与专注练习，展现简约的修行姿态。', '男士冥想瑜伽服 - 舒适与简约的修行选择', '专为男士设计的冥想瑜伽服装系列，采用宽松剪裁与柔软面料制作。我们的服装确保舒适与自由移动，帮助您在练习中深度放松与专注。面料采用有机棉、竹纤维等天然材料，透气吸汗，适合各种瑜伽、冥想、气功练习。款式包括宽松长裤、舒适上衣、套装等多种选择，展现简约的修行姿态。每件作品都经过精心设计，细节考究，为您的练习带来全方位的舒适体验，成为您精神实践的理想着装。', '男士瑜伽服, 冥想服装, 宽松长裤, 舒适上衣', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('911c580f-cae9-42b7-ba25-31f6494f3048', '365a40d4-a193-4a42-b756-1bd97d6ce679', 'zh-CN', '佛系T恤', '男士佛系主题T恤，融合佛教元素与现代设计，采用优质棉料制作，展现精神内涵与时尚风格，成为日常穿着的理想选择，传递平和与智慧。', '男士佛系T恤 - 精神内涵的时尚表达', '男士佛系主题T恤系列，融合佛教元素与现代设计。我们的T恤采用优质棉料制作，亲肤透气，版型修身。图案设计包括佛像、经文、莲花等多种宗教符号，展现精神内涵与艺术美感。这些T恤不仅是日常穿着的理想选择，更是表达个人信仰与追求平和的理想方式。每件作品都经过精心印刷，确保色彩鲜艳持久，图案细节清晰。适合各种场合穿着，为您的日常装扮增添文化深度与时尚风格，成为连接内心与外在的桥梁。', '佛系T恤, 佛教元素, 精神内涵, 日常穿着', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('df107009-3fb4-4e91-a6cf-87e68c8f46db', 'f61fdd9d-346b-4bf2-8680-ea4eeee167db', 'zh-CN', '上衣', '男士上衣系列，采用舒适面料与经典剪裁，展现简约与大气，适合多种场合穿着，成为衣橱中的百搭单品，彰显自然气质与个性风格。', '男士上衣 - 舒适与经典的日常选择', '男士上衣系列，采用舒适面料与经典剪裁制作。我们的上衣款式多样，包括宽松T恤、修身衬衫、柔软针织衫等，展现简约与大气。面料选择注重透气性与耐用性，适合日常穿着、冥想练习或休闲出行。每款上衣都经过精心设计，细节处理考究，能够轻松搭配各种下装，成为衣橱中的百搭单品。无论是追求休闲风格还是优雅气质，都能找到适合的选择，彰显自然气质与个性魅力。', '男士上衣, 舒适面料, 经典剪裁, 百搭配饰', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('6b3e3557-1abf-4720-983d-c6c999be97e2', '4a9e3456-33a2-4615-9b7e-fa6301c6cf17', 'zh-CN', '长裤', '男士长裤系列，采用舒适面料与修身剪裁，提供多种款式如直筒裤、宽松裤、瑜伽裤等，满足不同风格需求，为日常穿着与冥想练习提供理想选择，展现自然舒适与时尚风格。', '男士长裤 - 舒适与风格的完美结合', '男士长裤系列，采用柔软舒适的面料与修身剪裁制作。我们的长裤款式丰富，包括直筒裤、宽松裤、瑜伽裤、工装裤等，满足不同风格与需求。面料选择注重透气性与弹性，确保穿着舒适，适合日常穿着、冥想练习与各种活动。设计细节如多口袋、抽绳腰头、强化膝部等，提升实用与造型感。每条长裤都经过精细制作，确保版型稳定与品质优良。无论是追求休闲风格、运动装扮还是优雅气质，都能找到理想的款式，成为衣橱中的实用单品，展现自然舒适与时尚风格的完美结合。', '男士长裤, 舒适面料, 修身剪裁, 风格多样', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('7f9e256d-c8a7-4705-882d-5340cdc72c23', 'd4dbad47-4e7f-448e-be7b-ec461a4f2f5d', 'zh-CN', '外套', '男士外套系列，采用保暖面料与时尚设计，提供多种款式选择，从休闲夹克到优雅大衣，为不同季节与场合提供理想搭配，展现男性的稳重与时尚态度。', '男士外套 - 保暖与时尚的完美融合', '男士外套系列，采用高品质保暖面料与时尚设计制作。我们的外套款式多样，包括休闲夹克、连帽外套、修身大衣、皮草外套等，适合不同季节与场合穿着。设计注重细节，如精致刺绣、独特领口、功能性口袋等，展现男性的稳重与时尚态度。外套不仅提供出色的保暖性能，更通过精心剪裁与时尚元素提升整体造型。无论是日常通勤、冥想旅行还是社交活动，都能找到理想的搭配，成为您衣橱中的必备单品，为您的装扮增添层次感与风格亮点。', '男士外套, 保暖夹克, 优雅大衣, 时尚设计', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('75a095a9-94c0-424d-af7e-991fa1e8c0a4', '39cad863-d669-4cad-9d48-ef281329d233', 'zh-CN', '按活动分类', '根据不同活动场景设计的服装系列，包括瑜伽、冥想、太极等，确保每种活动都能找到合适的穿着选择，展现功能性与文化深度，支持身心实践的全方位需求。', '活动专属服装 - 功能性与文化的完美结合', '根据不同活动场景设计的服装系列，包括瑜伽、冥想、太极等。我们的活动专属服装采用功能性面料与专业剪裁，确保每种活动都能找到合适的穿着选择。瑜伽服装提供高弹力与透气性，冥想服装注重宽松舒适与宁静氛围，太极服装则结合传统元素与流畅动作需求。每件作品都融合文化深度与现代设计，支持身心实践的全方位需求。无论您是专业练习者还是初学者，都能在我们的系列中找到理想的服装，帮助提升练习效果，展现文化内涵与个人风格。', '活动服装, 瑜伽服装, 冥想服饰, 太极服装', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('9105f820-f382-4da7-b986-bbe6167dbbd1', '1fbe1c95-d916-4676-9514-e8e95ca7dd78', 'zh-CN', '瑜伽', '专为瑜伽练习设计的服装系列，采用高弹力面料与修身剪裁，确保舒适与自由移动，帮助深度拉伸与平衡练习，展现优雅的练习姿态。', '瑜伽服装 - 舒适与功能性的完美结合', '专为瑜伽练习设计的服装系列，采用高弹力、透气吸汗的面料与修身剪裁制作。我们的瑜伽服装确保舒适与自由移动，帮助您在练习中深度拉伸与保持平衡。款式包括紧身裤、运动背心、瑜伽外套等多种选择，满足不同瑜伽风格与环境需求。设计注重细节，如无缝拼接、加长腰头、抗菌处理等，提升穿着体验。每件作品都经过瑜伽大师测试，确保符合人体工学与瑜伽动作需求。无论是参加热瑜伽、哈他瑜伽、流动瑜伽还是冥想课程，都能找到理想的服装，成为您练习中的得力助手，展现优雅的练习姿态与专业精神。', '瑜伽服装, 高弹力面料, 修身剪裁, 舒适移动', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('07eb1325-3693-4407-90ae-2d5cee558396', '0afd7191-46da-42c5-ab2e-33757a7dec37', 'zh-CN', '冥想', '专为冥想练习设计的服装系列，采用宽松剪裁与柔软面料，创造宁静氛围，帮助放松身心，进入深度冥想状态，展现平和的修行姿态。', '冥想服装 - 宁静与舒适的修行选择', '专为冥想练习设计的服装系列，采用宽松剪裁与柔软面料制作。我们的冥想服装创造宁静氛围，帮助您放松身心，进入深度冥想状态。面料选择注重透气性与轻盈感，如有机棉、亚麻、丝绸等，确保长时间穿着的舒适度。款式包括宽松长裤、舒适上衣、长袍等多种选择，适合不同冥想姿势与环境。设计细节如宽松袖口、低领设计、纯色系等，减少视觉与身体干扰。每件作品都经过声学测试，确保面料摩擦声最小化，帮助维持冥想环境的安静。穿着冥想服装不仅是功能选择，更是心灵修行的外在表达，为您的精神实践增添和谐与专注。', '冥想服装, 宽松剪裁, 软软面料, 宁静氛围', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('225979c6-c9fa-4e47-b8a7-b291125c0fa3', 'a73ff6e6-cab0-4829-85b5-5e98c11ce7ae', 'zh-CN', '太极/气功', '专为太极与气功练习设计的服装系列，融合传统元素与现代面料，确保流畅动作与舒适穿着，展现东方美学与优雅气质，支持传统身心练习的完美表达。', '太极/气功服装 - 传统与现代的完美融合', '专为太极与气功练习设计的服装系列，融合传统元素与现代面料制作。我们的服装确保流畅动作与舒适穿着，采用柔软、轻盈、具有一定弹性的面料，如棉混纺、功能性丝绸等，适合缓慢而精准的动作需求。款式包括传统太极服、改良长袍、宽松裤装等多种选择，展现东方美学与优雅气质。设计细节如盘扣、立领、云肩等传统元素，与现代剪裁相结合，既尊重传统文化又符合当代审美。每件作品都经过太极大师与气功教练的测试，确保符合练习中的动作幅度与呼吸需求。穿着太极/气功服装，您将深入体验传统身心练习的精神内涵，展现优雅的练习姿态与文化传承。', '太极服装, 气功服饰, 传统元素, 东方美学', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('ed29ccc9-ce8f-4f1a-ab04-d0a89b913ad5', '4841d455-7b84-47ed-a3d2-93d5e42d407c', 'zh-CN', '配饰', '丰富多样的配饰系列，包括包包、围巾、毛毯等，采用优质材料与精致工艺，展现实用功能与时尚美感，为整体造型增添亮点与温暖感受。', '时尚配饰 - 实用与美学的完美结合', '丰富多样的配饰系列，包括包包、围巾、毛毯等。我们的配饰采用优质材料与精致工艺制作，展现实用功能与时尚美感。包包系列包括手提包、斜挎包、冥想包等多种类型，适合不同场合与需求。围巾采用柔软面料如羊绒、蚕丝、有机棉等制作，提供保暖与装饰双重功能。毛毯系列采用厚实面料，适合冥想垫、瑜伽铺巾、家居装饰等多种用途。每件配饰都经过精心设计，确保品质优良与细节完美，为您的整体造型增添亮点，带来温暖与舒适的使用体验。无论是作为礼物还是自用，这些配饰都能成为日常生活的实用伙伴与时尚声明。', '时尚配饰, 实用功能, 精致工艺, 保暖装饰', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('5598fbd5-eb33-436b-90c7-97ca51e97561', '70b7b4d8-8e9d-4c56-85dd-772c06b2fe42', 'zh-CN', '包包', '时尚包包系列，采用优质材料制作，设计多样，从简约手提包到多功能背包，满足不同场合与需求，展现个性风格与实用功能，成为出行的理想伴侣。', '时尚包包 - 个性风格的实用选择', '时尚包包系列，采用优质材料如皮革、帆布、再生纤维等制作。我们的包包设计多样，包括手提包、斜挎包、背包、冥想包等多种类型，满足不同场合与需求。注重功能性细节，如宽敞内部空间、多功能隔层、防水涂层、加固背带等，确保实用与耐用。设计风格从简约现代到民族传统，展现个性风格与文化深度。每个包包都经过严格质量检验，确保拉链顺畅、面料坚固、外观精致。无论是日常通勤、旅行探险还是冥想修行，都能找到理想的包包，成为您出行的得力助手，展现独特品味与生活态度。', '时尚包包, 优质材料, 功能设计, 个性风格', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('9f130878-eadc-4868-b549-f72503aea3a7', 'd17378c1-5046-4360-99ee-75182a26e5ec', 'zh-CN', '围巾+披肩', '柔软围巾与披肩系列，采用高级面料如羊绒、蚕丝、 modal 等制作，提供温暖与优雅的佩戴体验，成为季节转换与风格搭配的理想选择，展现女性的柔美与气质。', '柔软围巾与披肩 - 温暖与优雅的时尚单品', '柔软围巾与披肩系列，采用高级面料如羊绒、蚕丝、 modal、有机棉等制作。我们的围巾与披肩提供温暖与优雅的佩戴体验，适合季节转换与各种风格搭配。款式多样，包括窄围巾、大方巾、长披肩、短斗篷等多种选择，满足不同场合需求。设计注重色彩搭配与图案设计，从纯色经典到民族印花、几何图案等，展现女性的柔美与气质。围巾与披肩不仅具有保暖功能，更是整体造型的点睛之笔，能够瞬间提升穿搭的层次感与时尚度。每件作品都经过精细制作，确保面料柔软、色泽鲜艳、边缘整齐，成为衣橱中的百搭单品，为您的装扮增添无限魅力。', '柔软围巾, 高级面料, 优雅披肩, 温暖搭配', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('7991a119-6c43-4b73-99f5-2efbf11e6887', '09c86466-821a-44b2-9210-36a618d08a78', 'zh-CN', '毛毯', '舒适毛毯系列，采用厚实面料如羊毛、棉布、亚麻等制作，适合冥想垫、瑜伽铺巾、家居装饰等多种用途，为身心实践与日常休息提供温暖与舒适的支持。', '舒适毛毯 - 温暖与实用的家居选择', '舒适毛毯系列，采用厚实保暖的面料如羊毛、棉布、亚麻等制作。我们的毛毯适合多种用途，包括冥想垫、瑜伽铺巾、沙发毯、床毯等，为您的身心实践与日常休息提供温暖与舒适的体验。面料经过特殊处理，确保柔软度、透气性与耐用性，部分款式还具有抗菌、防螨等健康功能。设计风格多样，从简约纯色到民族图案、几何纹理等，适合不同家居装饰风格。每条毛毯都经过精细织造与质量检验，确保尺寸稳定、色彩牢固、触感优良。无论是作为冥想辅助工具、瑜伽练习铺巾还是家居装饰品，毛毯都能为您带来全方位的舒适感受，成为生活中的温暖伴侣。', '舒适毛毯, 厚实面料, 冥想垫毯, 家居装饰', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('be435ac7-cee7-48c9-a495-a93519bfadba', '1bc893b2-5227-4cd2-871d-10cdf3b89da4', 'zh-CN', '家宅饰品', '家宅饰品', '家宅饰品', '家宅饰品', '家宅饰品', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('8bbbf3b4-088c-497b-8dd6-026a426f2978', '0fb693d4-66d7-4633-9d09-1473c3038f6e', 'zh-CN', '佛像', '精美的佛像系列，包括释迦牟尼佛、笑佛、观音菩萨、象神等多种造型，采用优质材料制作，展现庄严与慈悲，为您的修行与家居带来神圣氛围。', '佛像系列 - 庄严慈悲的精神象征', '精美的佛像系列，包括释迦牟尼佛、笑佛、观音菩萨、象神等多种造型。我们的佛像采用黄铜、黑檀、水晶、树脂等优质材料制作，每尊佛像都经过细致雕刻与精细打磨，展现庄严与慈悲的神态。佛像不仅作为冥想修行的焦点，帮助集中注意力与净化心灵，更是家居装饰中的神圣元素，为您的空间带来宁静与祥和。每尊佛像都附有详细的背景介绍与摆放建议，帮助您深入了解其文化意义与精神价值，成为您修行道路上的重要伴侣。', '佛像系列, 庄严佛像, 慈悲神态, 修行焦点', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('2de2203d-83db-43d7-9b9a-9bec16c8ba93', '05e3d800-057d-497a-8916-e406dae5cfea', 'zh-CN', '释迦牟尼佛像', '释迦牟尼佛像系列，展现佛陀的庄严与智慧，采用传统工艺制作，适合冥想修行与家居供奉，成为精神觉悟的象征与文化传承的载体。', '释迦牟尼佛像 - 庄严智慧的觉悟象征', '释迦牟尼佛像系列，展现佛陀的庄严与智慧。我们的佛像采用传统工艺制作，遵循佛教经典的比例与特征，确保每尊佛像都符合宗教规范。材质包括黄铜、黑檀、水晶等多种选择，每尊佛像都经过精细打磨与开光加持，增强其灵性能量。释迦牟尼佛像适合冥想修行时作为观想对象，帮助修行者集中注意力、净化心灵、提升觉悟。同时，佛像也是家居供奉的理想选择，为您的空间带来神圣氛围与文化深度。每尊佛像都附有详细的经文解释与修行指导，帮助您深入理解佛教教义，走在觉悟之路上。', '释迦牟尼佛像, 庄严智慧, 冥想修行, 家居供奉', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('457f8bbe-f713-45bc-8474-14dece35e2c4', '07ae0908-da25-43cf-b1f1-82c3123b1ebe', 'zh-CN', '笑佛像', '笑佛像系列，展现弥勒佛的欢乐与富足寓意，采用圆润造型与温暖材质制作，为您的空间带来喜乐能量，成为吸引好运与繁荣的理想摆件。', '笑佛像 - 欢乐富足的喜乐象征', '笑佛像系列，展现弥勒佛的欢乐与富足寓意。我们的笑佛像采用圆润造型与温暖材质如黄铜、陶瓷、树脂等制作，展现弥勒佛大肚能容、笑口常开的亲切形象。每尊笑佛都经过精细雕刻，确保表情生动、细节丰富，传递喜乐能量与积极心态。笑佛像适合放置在客厅、办公室、店铺等空间，作为吸引好运与繁荣的理想摆件。在佛教传统中，弥勒佛象征着未来觉悟与世间欢乐，我们的笑佛像将这种精神内涵具象化，为您的生活空间带来正能量与美好祝福。', '笑佛像, 弥勒佛像, 欢乐寓意, 富足象征', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('87637b3e-3450-46eb-8dec-13588ce8d938', '8822a91d-d5e3-415e-b245-3725b3598b79', 'zh-CN', '观音菩萨像', '观音菩萨像系列，展现慈悲与救度的神圣形象，采用优雅造型与细腻工艺制作，为您的修行与家居带来安宁与庇护，成为心灵慰藉的源泉。', '观音菩萨像 - 慈悲救度的神圣象征', '观音菩萨像系列，展现慈悲与救度的神圣形象。我们的观音像采用优雅造型与细腻工艺制作，材质包括玉石、黑檀、琉璃、青铜等多种选择，每尊菩萨像都经过精心雕刻与打磨，展现柔和面容与慈悲眼神。观音菩萨在佛教中被视为慈悲的化身，能够救苦救难、回应众生祈求。我们的观音像不仅适合冥想修行时作为观想对象，帮助培养慈悲心与智慧，更是家居供奉的理想选择，为您的空间带来安宁与庇护。每尊观音像都附有详细的经文介绍与摆放建议，帮助您深入了解其精神内涵与文化价值，成为心灵慰藉与精神支持的重要象征。', '观音菩萨像, 慈悲救度, 宁静庇护, 精美雕刻', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('bac65f33-9e57-4220-8a67-5c4708b5a37b', 'be178bf7-c03b-48d8-9602-05b906ea6cba', 'zh-CN', '象神像', '象神像系列，展现象头神甘尼许的智慧与力量，采用传统造型与优质材料制作，帮助去除障碍，为您的生活与修行带来好运与成功。', '象神像 - 智慧力量的障碍消除者', '象神像系列，展现象头神甘尼许的智慧与力量。我们的象神像采用传统造型与优质材料如黄铜、黑檀、树脂等制作，每尊像都经过精细雕刻，展现甘尼许的特征：象头人身、大肚、多臂，手持各种法器。在印度教传统中，甘尼许被视为智慧之神、成功之神，能够消除障碍、带来好运。我们的象神像适合放置在入口处、书桌、冥想空间等位置，作为去除障碍、开启成功之路的神圣象征。每尊象神像都附有详细的神话背景与祈福方法，帮助您连接古老的智慧传统，为生活与修行带来积极能量与保护力量。', '象神像, 甘尼许, 智慧力量, 障碍消除', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('c3b734bf-d2b7-46d4-afcf-8dda6923d7a9', '648bd9e4-f161-4b86-9aaa-46a9486d5acf', 'zh-CN', '冥想瑜伽佛像', '冥想瑜伽佛像系列，展现佛菩萨的冥想姿态与瑜伽精神，采用稳定造型与和谐比例制作，为您的练习空间带来专注能量，成为修行的理想陪伴。', '冥想瑜伽佛像 - 专注能量的修行伴侣', '冥想瑜伽佛像系列，展现佛菩萨的冥想姿态与瑜伽精神。我们的佛像采用稳定造型与和谐比例制作，材质包括黄铜、黑檀、陶瓷等多种选择，每尊像都经过精细雕刻，展现平和坐姿与专注神态。这些佛像专为冥想与瑜伽练习空间设计，能够帮助创造宁静氛围，增强修行能量。佛像的稳定造型象征内心的平静与专注，适合放置在冥想角落、瑜伽垫旁或安静的书房中。每尊佛像都附有详细的修行指导与空间布置建议，帮助您打造理想的练习环境，成为您每日修行与自我探索的忠实伴侣，引导您走向内心的平衡与觉醒之路。', '冥想瑜伽佛像, 专注能量, 修行陪伴, 稳定造型', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('ec63c1a7-8dba-4983-9298-32095e3e3ab7', 'ae6c4361-2f5f-4133-80bb-a7c1fcb70588', 'zh-CN', '家宅饰品目录', '家居装饰与个人用品的精选分类，包括香薰炉、钥匙链、装饰品、禅意花园等多种实用与美观兼具的商品，为您的生活空间增添和谐与个性。', '家居装饰品类 - 和谐美观的生活选择', '家居装饰与个人用品的精选分类，包括香薰炉、钥匙链、装饰品、禅意花园等多种实用与美观兼具的商品。我们的产品经过精心挑选，融合传统工艺与现代设计，展现独特风格与卓越品质。香薰炉帮助净化空气、创造冥想氛围，钥匙链与车挂增添日常便利与个性表达，装饰品提升空间美感，禅意花园提供微型冥想焦点。每件商品都注重细节，确保使用体验优良，为您的生活空间增添和谐与个性，成为连接物质舒适与精神宁静的桥梁。', '家居装饰, 香薰炉, 装饰品, 禅意花园', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('ab2c82f2-8547-40a4-8052-4bd6756a74f9', 'ef5e5203-97df-468d-bfa0-2a3d64f4c1ca', 'zh-CN', '香薰炉与香料', '香薰炉与香料系列，采用优质材料制作香薰炉，搭配天然香料，帮助净化空间、提升意识，创造理想的冥想与生活氛围，展现嗅觉疗愈的力量。', '香薰炉与香料 - 净化空间的嗅觉疗愈', '香薰炉与香料系列，采用优质陶瓷、金属、石材等材料制作香薰炉，搭配天然植物香料。我们的香薰炉设计精美，实用耐用，香料种类丰富，包括沉香、檀香、藏香等多种传统配方。燃烧香料产生的烟雾与香气能够净化空间、提升意识、缓解压力、促进放松，是冥想、瑜伽、阅读等安静活动的理想伴侣。在许多文化中，香薰被视为连接物质世界与精神世界的桥梁，我们的产品将这种古老智慧带入现代生活，帮助您创造和谐宁静的氛围，提升日常生活品质。每套香薰产品都附有使用指南与香料搭配建议，确保您获得最佳的嗅觉疗愈体验。', '香薰炉, 天然香料, 空间净化, 嗅觉疗愈', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('d020e1d0-e33e-4b9d-9dff-a6cadcfbdbe0', 'c939f87d-6cd9-405a-9e7f-8b74ae1e2797', 'zh-CN', '钥匙链 + 车挂', '钥匙链与车挂系列，融合实用功能与个性设计，采用优质材料制作，展现时尚风格与文化元素，为日常出行增添便利与精神守护。', '钥匙链与车挂 - 实用与个性的随身伴侣', '钥匙链与车挂系列，融合实用功能与个性设计。我们的产品采用金属、皮革、宝石、佛像等多种材料制作，确保耐用性与美观度。设计风格多样，从简约现代到宗教文化，满足不同个性需求。钥匙链帮助整理钥匙，防止丢失，车挂则为您的爱车增添个性装饰与精神守护。许多款式融入佛教、印度教等文化元素，如佛像、六字真言、吉祥图案等，寓意平安、智慧、好运。这些小物件不仅是日常用品，更成为精神信念的随身表达，为您的出行带来便利与正能量，成为生活中的贴心伴侣与文化使者。', '钥匙链, 车挂饰品, 个性设计, 精神守护', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('5443fac9-254f-4e18-9f73-cb80df8ccdf4', '7604d919-b3dc-491f-bf9c-89d6657e7cd1', 'zh-CN', '装饰品', '家居装饰品系列，包括摆件、挂饰、储物用品等，采用多样材质与设计风格，为您的生活空间增添美感与个性，创造和谐舒适的居住环境。', '家居装饰品 - 美学与实用的完美结合', '家居装饰品系列，包括摆件、挂饰、储物用品等多种类型。我们的产品采用陶瓷、木材、金属、玻璃等多种材质制作，设计风格从现代简约到民族传统，满足不同家居装饰需求。装饰品不仅提升空间美感，更注重实用功能，如带储物空间的摆件、可调节的挂饰、兼具装饰与使用的托盘等。每件作品都经过精心设计与制作，确保品质优良与细节完美。摆放合适的装饰品能够反映居住者的个性与品味，为家居环境增添和谐能量，创造舒适宜人的生活氛围。我们的装饰品系列帮助您打造独特风格的居住空间，成为美学与实用的完美结合。', '家居装饰品, 摆件挂饰, 实用功能, 美学风格', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('c6477921-1e77-4ef8-9062-97107eff9bb8', '5894bde9-4f8b-48d7-871f-94e3d4e9641b', 'zh-CN', '冥想禅园', '微型禅意花园系列，通过砂石、小雕塑、植物等元素创造冥想焦点，培养专注与耐心，展现日本禅宗美学，为室内空间增添宁静与冥想氛围。', '冥想禅园 - 日本禅宗美学的室内冥想工具', '微型禅意花园系列，通过砂石、小雕塑、植物等元素创造冥想焦点。我们的禅园设计精美，采用优质材料如陶瓷盆、天然砂石、小型佛像、植物盆栽等制作，展现日本禅宗美学的核心要素。禅园通过简约的设计与自然元素的结合，帮助培养专注力与耐心，成为理想的冥想辅助工具。使用禅园时，您可以通过耙砂、摆放小景等互动方式，进入深度放松状态，体验禅修的宁静与智慧。这些禅园适合放置在书桌、窗台、边几等位置，为室内空间增添宁静氛围，成为日常冥想与精神修养的重要部分，连接自然与内心平静，展现东方美学的独特魅力。', '禅意花园, 禅宗美学, 冥想焦点, 日本文化', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('c321221c-3085-41f3-929e-cc18dd5be61d', 'a02c92e7-45c0-4543-abbb-3d20ca466f41', 'zh-CN', '可爱动物装饰', '可爱动物造型装饰品系列，以树脂、陶瓷等材质制作，展现动物的灵动与趣味，为家居增添活泼氛围，成为表达个性与爱心的理想装饰选择。', '可爱动物装饰 - 活泼趣味的个性表达', '可爱动物造型装饰品系列，以树脂、陶瓷、毛绒等多种材质制作。我们的产品展现动物的灵动与趣味，如猫咪、狗狗、兔子、狐狸等形象栩栩如生，表情丰富。设计风格从写实到卡通，满足不同审美需求。这些装饰品适合放置在客厅、卧室、儿童房、办公室等空间，为环境增添活泼氛围与温馨感受。可爱动物装饰不仅是家居摆件，更是情感表达的方式，能够唤起人们对自然与生命的热爱。每件作品都经过精心制作，确保安全无毒、手感优良，成为表达个性与爱心的理想选择，特别适合赠送动物爱好者与儿童，为生活带来欢乐与温暖。', '动物装饰, 可爱造型, 活泼氛围, 个性表达', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('3b6dc9b2-10c1-4361-a306-07edfecf6093', 'df2e0873-6539-47e8-9c4d-61c342204336', 'zh-CN', '八卦图', '风水八卦图系列，采用传统符号与色彩设计，帮助能量流动与空间布局，为家居与工作环境带来和谐与平衡，展现风水文化的应用智慧。', '风水八卦图 - 能量流动的空间指南', '风水八卦图系列，采用传统符号与色彩设计制作。我们的八卦图以优质丝绸、纸张、亚克力等材料呈现，展现完整的八卦符号与九宫格布局，部分产品还融入生肖、星宿等元素，增强风水应用效果。八卦图在风水实践中用于分析能量流动、指导空间布局，帮助平衡气场、提升运势。我们的八卦图提供多种尺寸与风格选择，适合挂在客厅、办公室、玄关等重要位置。每张八卦图都附有详细的使用指南与风水原理解释，帮助您正确应用这一古老智慧，为家居与工作环境带来和谐与平衡，成为连接传统文化与现代生活的实用工具。', '风水八卦图, 能量流动, 空间布局, 风水文化', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('d60b4b52-ab2f-462b-8c39-14208e27d391', '34dde886-3bee-402f-8f99-652d14634800', 'zh-CN', '茶杯', '精美茶杯系列，采用优质陶瓷、紫砂等材质制作，展现传统工艺与文化内涵，为品茶时刻带来愉悦体验，成为茶道与日常饮用的理想器具。', '精美茶杯 - 传统工艺的品茶享受', '精美茶杯系列，采用优质陶瓷、紫砂、玻璃等材质制作。我们的茶杯展现传统工艺的精湛技艺，从手工拉坯、雕刻到釉彩绘制，每一步都经过严格把关。设计风格包括简约现代、古典青花、日式和风、中式典雅等多种选择，满足不同文化背景与审美需求。茶杯不仅注重外观美感，更强调实用功能，如良好的握持感、适度的容量、优质的材质确保茶香纯正。品茶时使用精美茶杯，不仅提升饮用体验，更成为文化交流与精神享受的重要部分。我们的茶杯适合茶道爱好者、收藏家以及追求生活品质的人士，为您的品茶时刻增添传统韵味与现代美感。', '精美茶杯, 传统工艺, 品茶体验, 茶道器具', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('87b9cba8-f78c-4bec-b270-e8f7174f358b', '7c38698d-7db3-48e5-882f-76aee3bfd999', 'zh-CN', '扇子', '传统扇子系列，采用丝绸、纸张、竹木等材质制作，展现东方工艺与文化美学，为夏日带来清凉，成为文化传承与时尚装饰的理想结合。', '传统扇子 - 东方美学的清凉伴侣', '传统扇子系列，采用丝绸、纸张、竹木等优质材质制作。我们的扇子展现东方工艺的精湛技艺，包括手工绘画、刺绣、雕刻等多种装饰技法，呈现山水、花鸟、人物、吉祥图案等丰富题材。扇子类型涵盖折扇、团扇、羽扇等多种形式，适合不同场合与个人风格。在实用性方面，扇子为夏日带来自然清凉，同时作为一种文化符号，体现了东方智慧与审美情趣。我们的扇子不仅适合自用，更是赠送亲友、文化交流的理想礼物，帮助传承传统工艺，展现文化自信。每把扇子都经过精心包装与保养说明，确保长久使用，成为集实用与艺术于一体的文化瑰宝。', '传统扇子, 东方工艺, 文化美学, 夏日清凉', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('52cb4ce6-6594-472b-a4b4-f660eb36d30c', '1788419b-6f18-4467-808f-a73627806cb5', 'zh-CN', '风水琉璃', '风水琉璃摆件系列，采用彩色琉璃材质制作，融合风水原理与艺术设计，为家居与办公环境带来美观与能量调节，成为收藏与装饰的理想选择。', '风水琉璃 - 艺术与能量的和谐摆件', '风水琉璃摆件系列，采用优质彩色琉璃材质制作。我们的产品融合传统风水原理与现代艺术设计，展现独特的造型与色彩魅力。琉璃摆件种类丰富，包括水晶球、招财猫、转运轮、生肖造型等，每件作品都经过高温烧制、手工雕刻、精细打磨等多道工序，确保品质优良、光泽持久。在风水应用中，这些摆件能够调节气场、招财进宝、化解煞气，为环境带来正能量。同时，作为艺术品，它们提升空间美感，成为家居与办公装饰的亮点。我们的风水琉璃摆件适合收藏、赠送或作为风水调整工具，为您的生活空间增添和谐与美感，展现东方智慧与艺术创新的完美结合。', '风水琉璃, 能量调节, 艺术摆件, 招财装饰', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('1a61666f-9070-4c86-9ef4-76409f170c9b', '2e93a69c-6e21-41d7-9c9a-2031f7d7dbe6', 'zh-CN', '艺术品', '各类艺术品系列，包括绘画、雕塑、摄影作品等，展现艺术家的独特视角与文化深度，为您的空间带来艺术氛围，成为审美提升与文化传承的重要媒介。', '艺术作品 - 审美提升的文化珍品', '各类艺术品系列，包括绘画、雕塑、摄影作品等多种形式。我们的艺术品来自世界各地的新兴与知名艺术家，展现多元文化视角与独特创作理念。每件作品都经过严格筛选，确保艺术价值与品质优良。这些艺术品不仅美化空间，更传递深刻的思想与情感，帮助观赏者拓展审美视野，感受不同文化的魅力。我们提供多种尺寸、材质、风格的选择，适合家居、办公室、商业空间等多种环境。购买艺术品不仅是装饰选择，更是参与文化传承、支持艺术创作的方式，为您的生活与工作空间注入灵魂与个性，成为文化对话与审美提升的重要媒介。', '艺术作品, 绘画雕塑, 审美提升, 文化传承', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('8cabb0b6-fac3-4bb4-b8bf-6b5aa2df9d35', 'fb9a8a15-1b74-4c7c-93de-d096d99c9e3c', 'zh-CN', '畅销商品', '店内畅销商品精选，基于顾客喜爱与销售数据推荐，涵盖多个品类的热门产品，确保品质与价值，成为您选购的理想参考。', '畅销商品 - 顾客喜爱的精选推荐', '店内畅销商品精选，基于长期销售数据与顾客反馈推荐。我们的畅销榜单涵盖珠宝首饰、冥想用品、藏式传统、服装服饰、家居装饰等多个品类，确保每件产品都经过市场验证，品质优良，价值出众。这些热门商品反映了顾客的喜好趋势与实际需求，从实用性强的日常用品到具有文化内涵的特色礼品，满足不同购买目的。我们定期更新畅销榜单，确保推荐的商品保持新鲜度与相关性。选择畅销商品，您将获得可靠的质量保障与满意的使用体验，同时也能发现被广泛认可的优质产品，成为您选购时的理想参考指南。', '畅销商品, 热门产品, 品质保障, 顾客推荐', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('4b58c628-1566-44cd-a1ad-fbb50c3dcfca', '2da8dcb7-d0ed-41a0-bb38-ce78e8556e83', 'zh-CN', '家居装饰新品', '最新到货的家居装饰商品，精选当季流行趋势与创新设计，为您的生活空间带来新鲜感与时尚元素，展现个性风格与现代美感。', '家居装饰新品 - 时尚趋势的前沿选择', '最新到货的家居装饰商品系列，精选当季流行趋势与创新设计。我们的新品涵盖香薰炉、装饰画、摆件、储物盒、纺织品等多种类型，采用优质材料与精湛工艺制作，展现个性风格与现代美感。每件产品都经过趋势研究与精心挑选，确保符合当代审美与生活方式需求。新品装饰品为您的生活空间带来新鲜感，成为更新家居氛围的理想选择。我们定期推出新品，帮助您紧跟时尚潮流，打造独特而舒适的居住环境。无论是整体风格改造还是局部点缀，都能找到合适的商品，展现您的生活品味与个性主张。', '家居装饰新品, 流行趋势, 创新设计, 时尚元素', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('92357483-27ae-4061-92d2-07fdb495e3eb', '8a98ac0b-b89c-42df-9358-0440c264d2fc', 'zh-CN', '墙面艺术', '墙面装饰艺术系列，包括象征符号挂画、藏式经幡、唐卡等，展现文化深度与视觉美感，为室内空间增添艺术气息与精神氛围，成为墙面装饰的理想选择。', '墙面艺术 - 文化深度的视觉享受', '墙面装饰艺术系列，包括象征符号挂画、藏式经幡、唐卡、风景画等多种类型。我们的墙面艺术品展现丰富文化内涵与视觉美感，采用优质材料如丝绸、棉麻、宣纸、亚克力等制作，确保色彩鲜艳、质感优良、持久耐用。这些装饰品不仅美化墙面，更传递深刻的精神价值与文化故事，为室内空间增添艺术气息与精神氛围。例如，藏式经幡随风飘动传播祝福，唐卡展现佛教智慧，象征符号挂画表达个人信念。我们的墙面艺术适合各种空间，从客厅、卧室到冥想室、办公室，帮助您打造富有个性与文化深度的视觉焦点，成为连接物质空间与精神世界的桥梁。', '墙面装饰, 象征符号, 藏式经幡, 唐卡艺术', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('e9daeef8-69c5-4fa6-be62-a0ad70ecec8d', '05315d10-2e09-4b44-bfb9-826358b298e0', 'zh-CN', '象征符号墙面', '象征符号墙面装饰系列，以艺术形式展现文化与精神符号，帮助表达个人信念与价值观，为室内空间带来意义与美感，成为视觉焦点与精神表达的载体。', '象征符号墙面 - 个人信念的视觉表达', '象征符号墙面装饰系列，以艺术形式展现文化与精神符号。我们的产品包括画布印刷、丝绸刺绣、金属浮雕、木质雕刻等多种形式，内容涵盖佛教符号（如八宝、六字真言）、印度教标志（如奥姆符号）、东方哲学元素（如阴阳、八卦）、西方神秘学图案等。这些装饰品帮助您表达个人信念与价值观，为室内空间带来深刻意义与美感。每个符号都附有详细的文化解释与悬挂建议，确保您正确理解其内涵。象征符号墙面装饰不仅美化空间，更成为精神对话的媒介，为您的生活带来持续的启示与力量，成为每日视觉焦点与心灵滋养的源泉。', '象征符号, 个人信念, 文化标志, 视觉表达', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('0cc924c8-0da5-4c7f-b347-80b4311fcf0a', '0bb76b9a-0072-438d-83ed-a08822c36b1d', 'zh-CN', '艺术品', '各类墙面艺术品系列，包括绘画、摄影、版画等，展现艺术家的独特视角与创意表达，提升空间的艺术氛围，成为审美提升与文化探索的窗口。', '墙面艺术品 - 独特视角的视觉享受', '各类墙面艺术品系列，包括绘画、摄影、版画、浮雕等多种形式。我们的艺术品来自全球艺术家，展现多元文化视角与创意表达。每件作品都经过精心挑选，确保艺术价值与品质优良。这些墙面装饰提升空间的艺术氛围，帮助观赏者进入艺术家创造的视觉世界，感受不同的情感与思想。我们提供多种尺寸、材质、风格的选择，适合各种室内环境。购买艺术品不仅是装饰选择，更是参与文化对话、支持艺术创作的方式，为您的空间带来独特个性与深度美感，开启审美提升与文化探索的旅程。', '墙面艺术品, 绘画摄影, 创意表达, 艺术氛围', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('62282527-10d2-44f8-a9f9-8bcede5e6140', '5ffbe027-28cc-4772-bc7d-b0eb580e38f7', 'zh-CN', '藏式经幡', '藏式经幡墙面装饰系列，印有经文与吉祥图案的彩色布旗，随风飘动传播正能量，为环境增添神圣氛围与文化美感，成为独特的祈福象征。', '藏式经幡 - 随风传播的祈福象征', '藏式经幡墙面装饰系列，印有佛教经文与吉祥图案的彩色布旗。我们的经幡采用优质布料制作，色彩鲜艳持久，图案包括佛像、神兽、咒语等传统元素。经幡在藏族文化中象征神圣的祈祷，当它们随风飘动时 believed to spread spiritual messages and blessings。将经幡装饰在墙面上，不仅为环境增添神圣氛围与文化美感，更是一种参与藏族精神实践的方式。我们的经幡提供多种尺寸与长度选择，适合阳台、庭院、室内悬挂等多种场合。每套经幡都附有详细的使用指南与文化背景说明，帮助您深入了解其意义，正确悬挂以获得最佳效果，为您的空间带来和谐与安宁。', '藏式经幡, 祈福象征, 能量传播, 文化装饰', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('917b17f5-59db-4510-9b4c-ffeaeab25af5', 'f70cb395-36ee-45eb-9c24-863dde4390e8', 'zh-CN', '唐卡绘画', '传统唐卡绘画系列，以矿物颜料绘制佛像与藏族神话，展现精湛的绘画技艺与深厚的精神内涵，是藏族艺术的珍品，具有收藏与装饰价值。', '唐卡绘画 - 藏族艺术的精神珍品', '传统唐卡绘画系列，以矿物颜料精心绘制佛像与藏族神话场景。我们的唐卡由经验丰富的画师手工制作，遵循千年传统工艺，使用金箔、银箔、宝石粉末等珍贵材料，确保色彩鲜艳持久、线条细腻流畅。每幅唐卡都蕴含深厚的宗教意义与精神价值，展现佛菩萨的神圣形象与藏族宇宙观。唐卡不仅是艺术品，更是修行辅助工具，帮助观想与冥想。我们提供多种尺寸与题材选择，包括佛像、菩萨、护法、本尊等，适合家居供奉、寺庙装饰或艺术收藏。每幅唐卡都附有详细背景说明与保养指南，帮助您深入了解其文化内涵，珍藏这份来自雪域高原的艺术瑰宝，为生活空间带来神圣氛围与文化深度。', '唐卡绘画, 藏族艺术, 佛像唐卡, 艺术收藏', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('d8f1ecfd-ec54-4237-a104-831fe1c88a79', '6a3648ce-5e62-457d-926f-1b46e7d9da46', 'zh-CN', '风铃与铜铃', '风铃与铜铃墙面装饰系列，以金属材质制作，通过风的吹动产生悦耳声音，帮助净化空间，创造和谐氛围，成为听觉与视觉的双重享受。', '风铃与铜铃 - 和谐声音的墙面装饰', '风铃与铜铃墙面装饰系列，以金属材质精心制作。我们的产品包括传统风铃、管铃、铜铃等多种类型，设计融合文化元素与现代美感。风铃通过风的吹动产生悦耳声音，帮助净化空间、提升能量、创造和谐氛围。部分款式还可作为门帘或挂饰使用，兼具实用与装饰功能。风铃与铜铃不仅带来听觉享受，其金属光泽与精致造型也为墙面增添视觉美感。我们的风铃采用优质材料，确保声音清脆悠扬、结构稳固耐用。每件作品都经过声音调试与质量检验，确保您获得最佳的听觉与视觉体验，为您的室外与室内空间带来自然能量与艺术氛围，成为连接声音疗愈与家居装饰的完美媒介。', '风铃铜铃, 和谐声音, 空间净化, 视听享受', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('9e10bde2-21ca-49d9-98c5-e65e65622c9d', '046970d6-f118-49bd-92b0-382f407f9cc8', 'zh-CN', '礼物', '精心挑选的礼物系列，根据接收者与场合分类，包括个性化定制、首饰盒、电子礼券等多种选择，为您的送礼需求提供全方位解决方案，传递心意与文化价值。', '特色礼物系列 - 传递心意与文化价值', '精心挑选的礼物系列，根据接收者与场合分类。我们的礼物包括为女性、男性、情侣设计的专门系列，个性化定制服务满足独特需求，首饰盒与电子礼券提供更多便利选择。每件礼品都融合优质材质与精美设计，展现文化深度与艺术美感，确保您的心意得到完美表达。无论是生日、纪念日、节庆还是日常惊喜，我们都能帮助您找到合适的礼物，传递情感与祝福，成为您表达关怀的理想方式。', '特色礼物, 个性化定制, 首饰盒, 电子礼券', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('0950fd77-66c0-476a-8571-38e83da559dd', 'f7d3fef4-7fb6-4e13-8c2d-8c433e353743', 'zh-CN', '为女性', '专为女性设计的礼物系列，融合优雅与实用，涵盖珠宝、服饰、冥想用品等多种选择，展现对女性特质的深刻理解，成为表达关怀与欣赏的理想方式。', '女性礼物系列 - 优雅实用的贴心选择', '专为女性设计的礼物系列，融合优雅与实用元素。我们的女性礼物涵盖珠宝首饰、舒适服装、精美的冥想用品等多种品类，每件礼品都经过精心挑选，展现对女性特质的深刻理解。珠宝系列展现女性的柔美与魅力，服装系列注重舒适与风格，冥想用品帮助女性在繁忙生活中找到平静。这些礼物不仅是物质赠送，更是对女性内在价值的欣赏与尊重，成为表达关怀、爱意与敬意的理想选择，让每一位女性都感受到特别的对待与温暖的心意。', '女性礼物, 珠宝首饰, 舒适服装, 冥想用品', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('e825d542-9347-4673-8b70-a8c3cdcd0c36', '726e905f-253f-4e58-bc3d-828df2ae5fbc', 'zh-CN', '为男性', '专为男性设计的礼物系列，融合简约与力量感，提供珠宝、服饰、实用配饰等多种选择，展现阳刚气质与品味，成为表达尊重与欣赏的理想方式。', '男性礼物系列 - 简约力量的品味选择', '专为男性设计的礼物系列，融合简约设计与力量感。我们的男性礼物包括精致珠宝、舒适服装、实用配饰等多种选择，展现阳刚气质与高雅品味。珠宝系列注重细节与质感，服装系列强调合身与舒适，实用配饰如钱包、皮带、钥匙链等满足日常需求。这些礼物不仅是实用物品，更是对男性内在价值的认可与尊重，成为表达关怀、感谢与敬意的理想方式。无论是父亲、丈夫、朋友还是同事，都能在我们的系列中找到合适的礼物，传递您的心意与祝福。', '男性礼物, 精致珠宝, 舒适服装, 实用配饰', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('ee4e11e6-6970-41f6-95d1-dcb5fb17177b', '5d0f52db-3b7f-4431-9d2a-bed455939904', 'zh-CN', '为情侣', '专为情侣设计的礼物系列，展现浪漫与甜蜜，包括对戒、情侣装、双人冥想套装等，帮助表达爱意与承诺，成为关系升温与纪念时刻的理想选择。', '情侣礼物系列 - 浪漫甜蜜的爱情表达', '专为情侣设计的礼物系列，展现浪漫与甜蜜元素。我们的礼物包括对戒、情侣项链、情侣手链等珠宝系列，展现永恒的爱与承诺；情侣装如T恤、外套等展现默契与统一；双人冥想套装帮助情侣在精神层面建立更深连接。每件礼品都经过精心设计，注重细节与品质，为特别的日子增添难忘回忆。这些礼物不仅是物质赠送，更是情感交流与爱意表达的方式，帮助您向伴侣传递深刻的情感与珍惜之情，成为关系升温与纪念时刻的理想选择。', '情侣礼物, 对戒项链, 情侣装, 双人套装', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('18d1a117-b739-4004-80e7-b119551a01b1', '1d67e36f-5164-44ef-b476-f6954c707563', 'zh-CN', '个性化礼物', '个性化定制礼物系列，提供刻字、图案定制服务，打造独一无二的礼品，展现专属心意与特别记忆，成为表达独特情感的理想选择。', '个性化礼物 - 独一无二的情感表达', '个性化定制礼物系列，提供刻字、图案设计、材料选择等多种定制服务。我们的产品包括珠宝首饰、饰品盒、服装、冥想用品等，帮助您打造独一无二的礼品。每件礼品都经过精心制作，确保定制内容精确呈现，展现专属心意与特别记忆。个性化礼物不仅是物质赠送，更是情感交流的深度体现，能够让接收者感受到您的用心与关怀。无论是纪念日、生日还是特殊场合，定制礼物都能成为表达独特情感、传递珍贵记忆的理想方式，让每一份礼物都具有特殊意义与永恒价值。', '个性化定制, 刻字服务, 独特礼品, 情感表达', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('f68d5812-d079-4c52-b48a-2413591b9650', '7f149e82-5599-46e6-ad99-853bdf52c729', 'zh-CN', '礼物套装', '精选礼物套装系列，精心搭配多种商品，满足不同场合需求，提供便捷的送礼选择，展现全方位的关怀与品味，成为一站式礼物解决方案。', '礼物套装 - 精心搭配的全方位选择', '精选礼物套装系列，精心搭配多种商品，满足生日、节庆、纪念日等不同场合需求。我们的套装包括珠宝组合、冥想用品套装、香薰礼盒、服装配饰组合等多种类型，每套礼物都经过专业搭配，确保实用与美观并存。礼物套装的优势在于一站式解决您的送礼需求，节省挑选时间，同时通过精心组合展现全方位的关怀与品味。每套礼物都采用精美包装，提升整体质感，成为表达心意的理想选择。无论是家庭聚会、商务往来还是朋友间的情谊表达，都能找到合适的礼物套装，传递您的温暖与祝福。', '礼物套装, 精心搭配, 多样商品, 送礼选择', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('03dbc411-e7e6-4e32-87de-b018d7559ee0', '1044f952-b753-45bf-8f18-a7cca16e6cc0', 'zh-CN', '首饰盒', '精美首饰盒系列，采用优质材料制作，设计优雅实用，帮助收纳与展示珠宝，成为赠送首饰的理想配套，展现精致与呵护的心意。', '首饰盒 - 精致收纳的珠宝伴侣', '精美首饰盒系列，采用优质木材、皮革、丝绸等材料制作，展现优雅设计与实用功能。我们的首饰盒提供多种尺寸与风格选择，从简约现代到复古奢华，满足不同审美需求。内部结构精心设计，包括分隔层、抽屉、悬挂空间等，确保各类珠宝（戒指、耳环、项链、手链等）都能得到妥善收纳与保护。首饰盒不仅是实用物品，更是赠送珠宝的理想配套，展现您的精致与呵护之心。我们还提供定制服务，如刻字、专属标志等，让首饰盒成为具有纪念意义的礼物。无论是作为自我收藏还是赠送他人，首饰盒都将成为珠宝的完美归宿，增添使用时的愉悦体验。', '首饰盒, 收纳展示, 精致设计, 定制服务', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');
INSERT INTO "public"."product_category_translations" VALUES ('082ae8a6-cc95-49e8-9a11-14616a5dbb9d', '9036b668-0295-4d9d-9117-8418e939e36f', 'zh-CN', '电子礼券', '电子礼券系列，提供便捷的数字礼物选择，可自定义金额与祝福语，通过邮件或短信发送，成为快速传递心意的理想方式，适合各种紧急与特殊送礼需求。', '电子礼券 - 快捷方便的心意传递', '电子礼券系列，提供便捷的数字礼物选择。我们的礼券允许您自定义金额、选择祝福模板、添加个人留言，通过邮件或短信即时发送给接收者。电子礼券适用于各种场合，如生日、节日、纪念日、商务馈赠等，尤其适合紧急送礼需求或无法当面赠送的情况。接收者可在礼券有效期内自由选购网站上的任何商品，确保礼物符合其个人喜好。电子礼券不仅环保便捷，更展现出送礼者的 thoughtful 与现代化，成为快速传递心意的理想方式。我们提供多种设计精美的礼券模板，确保您的心意得到完美表达。', '电子礼券, 数字礼物, 自定义金额, 即时发送', '2025-05-27 19:00:22.571064', '2025-05-27 19:00:22.571064');

-- ----------------------------
-- Table structure for product_images
-- ----------------------------
DROP TABLE IF EXISTS "public"."product_images";
CREATE TABLE "public"."product_images" (
  "id" uuid NOT NULL,
  "product_id" uuid NOT NULL,
  "image_url" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "image_type" "public"."imagetype" NOT NULL,
  "alt_text" varchar(255) COLLATE "pg_catalog"."default",
  "title" varchar(255) COLLATE "pg_catalog"."default",
  "description" text COLLATE "pg_catalog"."default",
  "width" int4,
  "height" int4,
  "file_size" int4,
  "sort_order" int4,
  "is_active" bool,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL,
  "duration" int4,
  "thumbnail_url" varchar(255) COLLATE "pg_catalog"."default",
  "is_video" bool NOT NULL DEFAULT false,
  "video_format" varchar(10) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "public"."product_images"."image_url" IS '图片/视频URL';
COMMENT ON COLUMN "public"."product_images"."image_type" IS '媒体类型';
COMMENT ON COLUMN "public"."product_images"."alt_text" IS '替代文本，用于SEO和无障碍访问';
COMMENT ON COLUMN "public"."product_images"."title" IS '图片/视频标题';
COMMENT ON COLUMN "public"."product_images"."description" IS '图片/视频描述';
COMMENT ON COLUMN "public"."product_images"."width" IS '图片宽度/视频宽度(像素)';
COMMENT ON COLUMN "public"."product_images"."height" IS '图片高度/视频高度(像素)';
COMMENT ON COLUMN "public"."product_images"."file_size" IS '文件大小(KB)';
COMMENT ON COLUMN "public"."product_images"."sort_order" IS '排序顺序';
COMMENT ON COLUMN "public"."product_images"."is_active" IS '是否激活';
COMMENT ON COLUMN "public"."product_images"."duration" IS '视频时长(秒)';
COMMENT ON COLUMN "public"."product_images"."thumbnail_url" IS '视频缩略图URL';
COMMENT ON COLUMN "public"."product_images"."is_video" IS '是否为视频文件';
COMMENT ON COLUMN "public"."product_images"."video_format" IS '视频格式(mp4, webm等)';

-- ----------------------------
-- Records of product_images
-- ----------------------------
INSERT INTO "public"."product_images" VALUES ('83f8c7b3-d143-45c7-a476-621cc4392628', '8412d590-9bf6-47c9-a5fc-302f1847513c', '/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/a6f221c6adf448859ca0f253add9f548_1748425530.webp', 'MAIN', '玉石吊坠鱼', '玉石吊坠鱼', '玉石吊坠鱼', 720, 720, 60, 0, 't', '2025-05-28 09:45:30.629878', '2025-05-28 09:46:19.722734', NULL, NULL, 'f', NULL);
INSERT INTO "public"."product_images" VALUES ('c73172ee-d119-423f-ba61-9857acc349bb', '8412d590-9bf6-47c9-a5fc-302f1847513c', '/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/a5c5a8dbca474152b314ecb2915d8988_1748425649.webp', 'GALLERY', '玉石吊坠鱼', '玉石吊坠鱼', '玉石吊坠鱼', 720, 720, 61, 0, 't', '2025-05-28 09:47:29.971085', '2025-05-28 09:49:06.183366', NULL, NULL, 'f', NULL);
INSERT INTO "public"."product_images" VALUES ('66046e29-04ba-40e2-8aab-1931940df225', '8412d590-9bf6-47c9-a5fc-302f1847513c', '/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/9e589273f86b468db2d863cada3a7d18_1748425714.webp', 'GALLERY', '玉石吊坠鱼', '玉石吊坠鱼', '玉石吊坠鱼', 720, 720, 50, 1, 't', '2025-05-28 09:48:34.342798', '2025-05-28 09:49:15.384527', NULL, NULL, 'f', NULL);
INSERT INTO "public"."product_images" VALUES ('2ee0cf13-0c24-461f-b836-aadb2c375094', '8412d590-9bf6-47c9-a5fc-302f1847513c', '/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/25ad9bd6afd04a07bb810561ca820486_1748426096.webp', 'GALLERY', NULL, NULL, NULL, 720, 720, 13, 0, 't', '2025-05-28 09:54:56.45004', '2025-05-28 09:54:56.45004', NULL, NULL, 'f', NULL);
INSERT INTO "public"."product_images" VALUES ('1c8713cf-3e36-4526-9d7a-013e095f33e8', '8412d590-9bf6-47c9-a5fc-302f1847513c', '/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/a4a4b766a9f74265aadc2bcced9fea1d_1748426117.webp', 'DETAIL', '玉石吊坠材质', '玉石吊坠材质', '吊坠原材料图片', 720, 720, 52, 0, 't', '2025-05-28 09:55:17.25215', '2025-05-28 09:56:04.193133', NULL, NULL, 'f', NULL);
INSERT INTO "public"."product_images" VALUES ('ceb75feb-149d-4035-9f7d-0b0bc3a7d1ff', '8412d590-9bf6-47c9-a5fc-302f1847513c', '/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/b6fc66f2c9f844cdb18961bf42ad8afd_1748428631.mp4', 'GALLERY', NULL, NULL, NULL, 720, 1280, 1675, 0, 't', '2025-05-28 10:37:12.071633', '2025-05-28 10:37:12.071633', 8, NULL, 't', 'mp4');
INSERT INTO "public"."product_images" VALUES ('2a57f685-2cc0-460e-bb4c-5cbd350e5b27', '4ed2ac2e-70c9-4679-a445-4076bf406fcd', '/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/a6f221c6adf448859ca0f253add9f548_1748425530.webp', 'MAIN', '玉石吊坠鱼', '玉石吊坠鱼', '玉石吊坠鱼', 720, 720, 60, 0, 't', '2025-06-06 00:14:00.925528', '2025-06-06 00:14:00.925528', NULL, NULL, 'f', NULL);
INSERT INTO "public"."product_images" VALUES ('7e8eb08f-34bf-432e-95b0-035b0045f4d7', '4ed2ac2e-70c9-4679-a445-4076bf406fcd', '/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/a5c5a8dbca474152b314ecb2915d8988_1748425649.webp', 'GALLERY', '玉石吊坠鱼', '玉石吊坠鱼', '玉石吊坠鱼', 720, 720, 61, 0, 't', '2025-06-06 00:14:00.926048', '2025-06-06 00:14:00.926048', NULL, NULL, 'f', NULL);
INSERT INTO "public"."product_images" VALUES ('c48d47a3-f2bd-461e-b8cb-b617036d73e6', '4ed2ac2e-70c9-4679-a445-4076bf406fcd', '/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/9e589273f86b468db2d863cada3a7d18_1748425714.webp', 'GALLERY', '玉石吊坠鱼', '玉石吊坠鱼', '玉石吊坠鱼', 720, 720, 50, 1, 't', '2025-06-06 00:14:00.926048', '2025-06-06 00:14:00.926048', NULL, NULL, 'f', NULL);
INSERT INTO "public"."product_images" VALUES ('936e544e-e2f4-405e-a08d-d38373b33996', '4ed2ac2e-70c9-4679-a445-4076bf406fcd', '/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/25ad9bd6afd04a07bb810561ca820486_1748426096.webp', 'GALLERY', NULL, NULL, NULL, 720, 720, 13, 0, 't', '2025-06-06 00:14:00.926048', '2025-06-06 00:14:00.926048', NULL, NULL, 'f', NULL);
INSERT INTO "public"."product_images" VALUES ('35128ebb-3f01-478b-a881-d91346b3670b', '4ed2ac2e-70c9-4679-a445-4076bf406fcd', '/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/a4a4b766a9f74265aadc2bcced9fea1d_1748426117.webp', 'DETAIL', '玉石吊坠材质', '玉石吊坠材质', '吊坠原材料图片', 720, 720, 52, 0, 't', '2025-06-06 00:14:00.926048', '2025-06-06 00:14:00.926048', NULL, NULL, 'f', NULL);
INSERT INTO "public"."product_images" VALUES ('811bd0da-fbf9-47bf-8fc5-9a143762d3bd', '4ed2ac2e-70c9-4679-a445-4076bf406fcd', '/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/b6fc66f2c9f844cdb18961bf42ad8afd_1748428631.mp4', 'GALLERY', NULL, NULL, NULL, 720, 1280, 1675, 0, 't', '2025-06-06 00:14:00.926048', '2025-06-06 00:14:00.926048', 8, NULL, 't', 'mp4');
INSERT INTO "public"."product_images" VALUES ('1578e76a-fa93-4486-8c1b-48afd4317f32', 'bed054b6-14cc-43fc-98d2-00ad7d14170b', '/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/a6f221c6adf448859ca0f253add9f548_1748425530.webp', 'MAIN', '玉石吊坠鱼', '玉石吊坠鱼', '玉石吊坠鱼', 720, 720, 60, 0, 't', '2025-06-06 00:14:00.998361', '2025-06-06 00:14:00.998361', NULL, NULL, 'f', NULL);
INSERT INTO "public"."product_images" VALUES ('7fb66efe-756f-43c8-a05e-d5e052fb9c66', 'bed054b6-14cc-43fc-98d2-00ad7d14170b', '/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/a5c5a8dbca474152b314ecb2915d8988_1748425649.webp', 'GALLERY', '玉石吊坠鱼', '玉石吊坠鱼', '玉石吊坠鱼', 720, 720, 61, 0, 't', '2025-06-06 00:14:00.99936', '2025-06-06 00:14:00.99936', NULL, NULL, 'f', NULL);
INSERT INTO "public"."product_images" VALUES ('4d768e1c-6214-41d9-8bc2-3dea6fa23e87', 'bed054b6-14cc-43fc-98d2-00ad7d14170b', '/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/9e589273f86b468db2d863cada3a7d18_1748425714.webp', 'GALLERY', '玉石吊坠鱼', '玉石吊坠鱼', '玉石吊坠鱼', 720, 720, 50, 1, 't', '2025-06-06 00:14:00.99936', '2025-06-06 00:14:00.99936', NULL, NULL, 'f', NULL);
INSERT INTO "public"."product_images" VALUES ('a9d34c93-6498-479b-bef8-dbf2fe8a6bf3', 'bed054b6-14cc-43fc-98d2-00ad7d14170b', '/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/25ad9bd6afd04a07bb810561ca820486_1748426096.webp', 'GALLERY', NULL, NULL, NULL, 720, 720, 13, 0, 't', '2025-06-06 00:14:00.99936', '2025-06-06 00:14:00.99936', NULL, NULL, 'f', NULL);
INSERT INTO "public"."product_images" VALUES ('5e0d34db-6003-425c-a40c-1cf5ec66e051', 'bed054b6-14cc-43fc-98d2-00ad7d14170b', '/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/a4a4b766a9f74265aadc2bcced9fea1d_1748426117.webp', 'DETAIL', '玉石吊坠材质', '玉石吊坠材质', '吊坠原材料图片', 720, 720, 52, 0, 't', '2025-06-06 00:14:00.99936', '2025-06-06 00:14:00.99936', NULL, NULL, 'f', NULL);
INSERT INTO "public"."product_images" VALUES ('0df38a88-32ea-41d9-8f04-efbc8c0e3176', 'bed054b6-14cc-43fc-98d2-00ad7d14170b', '/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/b6fc66f2c9f844cdb18961bf42ad8afd_1748428631.mp4', 'GALLERY', NULL, NULL, NULL, 720, 1280, 1675, 0, 't', '2025-06-06 00:14:00.99936', '2025-06-06 00:14:00.99936', 8, NULL, 't', 'mp4');
INSERT INTO "public"."product_images" VALUES ('f5eb5be5-b7f7-41bc-b56e-d45a616102fb', '10893657-5b79-4a06-852b-5b5358e447c7', '/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/a6f221c6adf448859ca0f253add9f548_1748425530.webp', 'MAIN', '玉石吊坠鱼', '玉石吊坠鱼', '玉石吊坠鱼', 720, 720, 60, 0, 't', '2025-06-06 00:14:01.055741', '2025-06-06 00:14:01.055741', NULL, NULL, 'f', NULL);
INSERT INTO "public"."product_images" VALUES ('c5900039-2cae-42c6-a5a9-e00fc9fb3ff8', '10893657-5b79-4a06-852b-5b5358e447c7', '/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/a5c5a8dbca474152b314ecb2915d8988_1748425649.webp', 'GALLERY', '玉石吊坠鱼', '玉石吊坠鱼', '玉石吊坠鱼', 720, 720, 61, 0, 't', '2025-06-06 00:14:01.055741', '2025-06-06 00:14:01.055741', NULL, NULL, 'f', NULL);
INSERT INTO "public"."product_images" VALUES ('1327d8fc-2ca1-43b6-9d7c-33a0e5ee78ac', '10893657-5b79-4a06-852b-5b5358e447c7', '/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/9e589273f86b468db2d863cada3a7d18_1748425714.webp', 'GALLERY', '玉石吊坠鱼', '玉石吊坠鱼', '玉石吊坠鱼', 720, 720, 50, 1, 't', '2025-06-06 00:14:01.055741', '2025-06-06 00:14:01.055741', NULL, NULL, 'f', NULL);
INSERT INTO "public"."product_images" VALUES ('c18a2b2d-ee8d-4b97-8a11-66412055a16d', '10893657-5b79-4a06-852b-5b5358e447c7', '/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/25ad9bd6afd04a07bb810561ca820486_1748426096.webp', 'GALLERY', NULL, NULL, NULL, 720, 720, 13, 0, 't', '2025-06-06 00:14:01.055741', '2025-06-06 00:14:01.055741', NULL, NULL, 'f', NULL);
INSERT INTO "public"."product_images" VALUES ('3b7231f9-a3bb-4422-81af-232ce4a1a7e3', '10893657-5b79-4a06-852b-5b5358e447c7', '/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/a4a4b766a9f74265aadc2bcced9fea1d_1748426117.webp', 'DETAIL', '玉石吊坠材质', '玉石吊坠材质', '吊坠原材料图片', 720, 720, 52, 0, 't', '2025-06-06 00:14:01.055741', '2025-06-06 00:14:01.055741', NULL, NULL, 'f', NULL);
INSERT INTO "public"."product_images" VALUES ('d157724b-0ff6-45cd-86c7-ab4b31c83757', '10893657-5b79-4a06-852b-5b5358e447c7', '/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/b6fc66f2c9f844cdb18961bf42ad8afd_1748428631.mp4', 'GALLERY', NULL, NULL, NULL, 720, 1280, 1675, 0, 't', '2025-06-06 00:14:01.055741', '2025-06-06 00:14:01.055741', 8, NULL, 't', 'mp4');
INSERT INTO "public"."product_images" VALUES ('fcaa7894-31e7-4b0e-91f8-86df115152da', 'dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/a6f221c6adf448859ca0f253add9f548_1748425530.webp', 'MAIN', '玉石吊坠鱼', '玉石吊坠鱼', '玉石吊坠鱼', 720, 720, 60, 0, 't', '2025-06-06 00:14:01.110297', '2025-06-06 00:14:01.110297', NULL, NULL, 'f', NULL);
INSERT INTO "public"."product_images" VALUES ('27f49400-d298-497e-8afa-a84c89c2095d', 'dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/a5c5a8dbca474152b314ecb2915d8988_1748425649.webp', 'GALLERY', '玉石吊坠鱼', '玉石吊坠鱼', '玉石吊坠鱼', 720, 720, 61, 0, 't', '2025-06-06 00:14:01.110297', '2025-06-06 00:14:01.110297', NULL, NULL, 'f', NULL);
INSERT INTO "public"."product_images" VALUES ('596f330e-a521-4ec8-b7aa-b4ed39665e34', 'dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/9e589273f86b468db2d863cada3a7d18_1748425714.webp', 'GALLERY', '玉石吊坠鱼', '玉石吊坠鱼', '玉石吊坠鱼', 720, 720, 50, 1, 't', '2025-06-06 00:14:01.110297', '2025-06-06 00:14:01.110297', NULL, NULL, 'f', NULL);
INSERT INTO "public"."product_images" VALUES ('74cda399-1856-4f5f-97ee-c339d5229e7a', 'dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/25ad9bd6afd04a07bb810561ca820486_1748426096.webp', 'GALLERY', NULL, NULL, NULL, 720, 720, 13, 0, 't', '2025-06-06 00:14:01.111297', '2025-06-06 00:14:01.111297', NULL, NULL, 'f', NULL);
INSERT INTO "public"."product_images" VALUES ('17f3b895-7259-448f-b1fd-6977f4e9f80d', 'dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/a4a4b766a9f74265aadc2bcced9fea1d_1748426117.webp', 'DETAIL', '玉石吊坠材质', '玉石吊坠材质', '吊坠原材料图片', 720, 720, 52, 0, 't', '2025-06-06 00:14:01.111297', '2025-06-06 00:14:01.111297', NULL, NULL, 'f', NULL);
INSERT INTO "public"."product_images" VALUES ('12a14774-9370-4180-b73e-95787a5a05eb', 'dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '/static/uploads/product-images/8412d590-9bf6-47c9-a5fc-302f1847513c/b6fc66f2c9f844cdb18961bf42ad8afd_1748428631.mp4', 'GALLERY', NULL, NULL, NULL, 720, 1280, 1675, 0, 't', '2025-06-06 00:14:01.111297', '2025-06-06 00:14:01.111297', 8, NULL, 't', 'mp4');

-- ----------------------------
-- Table structure for product_intent
-- ----------------------------
DROP TABLE IF EXISTS "public"."product_intent";
CREATE TABLE "public"."product_intent" (
  "product_id" uuid NOT NULL,
  "intent_id" uuid NOT NULL
)
;

-- ----------------------------
-- Records of product_intent
-- ----------------------------

-- ----------------------------
-- Table structure for product_intents
-- ----------------------------
DROP TABLE IF EXISTS "public"."product_intents";
CREATE TABLE "public"."product_intents" (
  "id" uuid NOT NULL,
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "slug" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default",
  "icon_url" varchar(255) COLLATE "pg_catalog"."default",
  "banner_url" varchar(255) COLLATE "pg_catalog"."default",
  "color_code" varchar(30) COLLATE "pg_catalog"."default",
  "is_active" bool,
  "is_featured" bool,
  "sort_order" int4,
  "seo_title" varchar(255) COLLATE "pg_catalog"."default",
  "seo_description" varchar(500) COLLATE "pg_catalog"."default",
  "seo_keywords" varchar(255) COLLATE "pg_catalog"."default",
  "cultural_significance" text COLLATE "pg_catalog"."default",
  "spiritual_meaning" text COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."product_intents"."name" IS '意图名称';
COMMENT ON COLUMN "public"."product_intents"."slug" IS '意图别名，用于URL';
COMMENT ON COLUMN "public"."product_intents"."description" IS '意图描述';
COMMENT ON COLUMN "public"."product_intents"."icon_url" IS '意图图标URL';
COMMENT ON COLUMN "public"."product_intents"."banner_url" IS '意图横幅图片URL';
COMMENT ON COLUMN "public"."product_intents"."color_code" IS '意图颜色代码';
COMMENT ON COLUMN "public"."product_intents"."is_active" IS '是否激活';
COMMENT ON COLUMN "public"."product_intents"."is_featured" IS '是否推荐意图';
COMMENT ON COLUMN "public"."product_intents"."sort_order" IS '排序顺序';
COMMENT ON COLUMN "public"."product_intents"."seo_title" IS 'SEO标题';
COMMENT ON COLUMN "public"."product_intents"."seo_description" IS 'SEO描述';
COMMENT ON COLUMN "public"."product_intents"."seo_keywords" IS 'SEO关键词';
COMMENT ON COLUMN "public"."product_intents"."cultural_significance" IS '文化意义';
COMMENT ON COLUMN "public"."product_intents"."spiritual_meaning" IS '精神含义';

-- ----------------------------
-- Records of product_intents
-- ----------------------------

-- ----------------------------
-- Table structure for product_inventories
-- ----------------------------
DROP TABLE IF EXISTS "public"."product_inventories";
CREATE TABLE "public"."product_inventories" (
  "id" uuid NOT NULL,
  "product_id" uuid NOT NULL,
  "sku_id" uuid,
  "quantity" int4 NOT NULL,
  "reserved_quantity" int4 NOT NULL,
  "alert_threshold" int4,
  "ideal_quantity" int4,
  "reorder_point" int4,
  "reorder_quantity" int4,
  "is_in_stock" bool,
  "is_managed" bool,
  "location" varchar(50) COLLATE "pg_catalog"."default",
  "notes" text COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."product_inventories"."quantity" IS '可用库存数量';
COMMENT ON COLUMN "public"."product_inventories"."reserved_quantity" IS '已预留数量（已下单未发货）';
COMMENT ON COLUMN "public"."product_inventories"."alert_threshold" IS '库存预警阈值';
COMMENT ON COLUMN "public"."product_inventories"."ideal_quantity" IS '理想库存量';
COMMENT ON COLUMN "public"."product_inventories"."reorder_point" IS '重新订货点';
COMMENT ON COLUMN "public"."product_inventories"."reorder_quantity" IS '重新订货数量';
COMMENT ON COLUMN "public"."product_inventories"."is_in_stock" IS '是否有库存';
COMMENT ON COLUMN "public"."product_inventories"."is_managed" IS '是否进行库存管理';
COMMENT ON COLUMN "public"."product_inventories"."location" IS '库存位置编码';
COMMENT ON COLUMN "public"."product_inventories"."notes" IS '备注信息';

-- ----------------------------
-- Records of product_inventories
-- ----------------------------
INSERT INTO "public"."product_inventories" VALUES ('81c949d7-bfb9-4861-80fd-ca120b6d27bd', '8412d590-9bf6-47c9-a5fc-302f1847513c', '4fe91b37-7bf8-4973-8411-391175eeeb96', 50, 0, 5, NULL, NULL, NULL, 't', 't', NULL, NULL, '2025-05-30 05:59:52.609142', '2025-05-30 05:59:52.609142');
INSERT INTO "public"."product_inventories" VALUES ('77b58355-5833-4b8c-bce3-0aea30d908c7', '4ed2ac2e-70c9-4679-a445-4076bf406fcd', '55d21ca1-488e-49f1-adb7-727a491de7f8', 50, 0, 5, NULL, NULL, NULL, 't', 't', NULL, NULL, '2025-06-06 00:14:00.926574', '2025-06-06 00:14:00.926574');
INSERT INTO "public"."product_inventories" VALUES ('265cecb0-f6f1-447f-b30e-6f58d36cbc63', 'bed054b6-14cc-43fc-98d2-00ad7d14170b', 'c4d4aab9-825c-45c4-a182-3b7160a453da', 50, 0, 5, NULL, NULL, NULL, 't', 't', NULL, NULL, '2025-06-06 00:14:00.99936', '2025-06-06 00:14:00.99936');
INSERT INTO "public"."product_inventories" VALUES ('43cdeebe-730d-4792-b848-f8751ec0df69', '10893657-5b79-4a06-852b-5b5358e447c7', '38ee75e2-ee3d-4447-808d-ea3048eaacb8', 50, 0, 5, NULL, NULL, NULL, 't', 't', NULL, NULL, '2025-06-06 00:14:01.055741', '2025-06-06 00:14:01.055741');
INSERT INTO "public"."product_inventories" VALUES ('3dfdebf7-d7eb-4d86-a7eb-508291f67be0', 'dffc8901-296d-4e26-88e4-a2c9ccc4ce51', '6275b947-32df-4f92-851c-fb4070dcdd60', 50, 0, 5, NULL, NULL, NULL, 't', 't', NULL, NULL, '2025-06-06 00:14:01.111297', '2025-06-06 00:14:01.111297');

-- ----------------------------
-- Table structure for product_material
-- ----------------------------
DROP TABLE IF EXISTS "public"."product_material";
CREATE TABLE "public"."product_material" (
  "product_id" uuid NOT NULL,
  "material_id" uuid NOT NULL
)
;

-- ----------------------------
-- Records of product_material
-- ----------------------------

-- ----------------------------
-- Table structure for product_materials
-- ----------------------------
DROP TABLE IF EXISTS "public"."product_materials";
CREATE TABLE "public"."product_materials" (
  "id" uuid NOT NULL,
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "slug" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "material_type" "public"."materialtype" NOT NULL,
  "description" text COLLATE "pg_catalog"."default",
  "icon_url" varchar(255) COLLATE "pg_catalog"."default",
  "image_url" varchar(255) COLLATE "pg_catalog"."default",
  "parent_id" uuid,
  "properties" text COLLATE "pg_catalog"."default",
  "origin_locations" text COLLATE "pg_catalog"."default",
  "care_instructions" text COLLATE "pg_catalog"."default",
  "cultural_significance" text COLLATE "pg_catalog"."default",
  "energy_properties" text COLLATE "pg_catalog"."default",
  "is_active" bool,
  "is_featured" bool,
  "sort_order" int4,
  "seo_title" varchar(255) COLLATE "pg_catalog"."default",
  "seo_description" varchar(500) COLLATE "pg_catalog"."default",
  "seo_keywords" varchar(255) COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."product_materials"."name" IS '材质名称';
COMMENT ON COLUMN "public"."product_materials"."slug" IS '材质别名，用于URL';
COMMENT ON COLUMN "public"."product_materials"."material_type" IS '材质类型';
COMMENT ON COLUMN "public"."product_materials"."description" IS '材质描述';
COMMENT ON COLUMN "public"."product_materials"."icon_url" IS '材质图标URL';
COMMENT ON COLUMN "public"."product_materials"."image_url" IS '材质图片URL';
COMMENT ON COLUMN "public"."product_materials"."parent_id" IS '父材质ID';
COMMENT ON COLUMN "public"."product_materials"."properties" IS '材质特性';
COMMENT ON COLUMN "public"."product_materials"."origin_locations" IS '原产地';
COMMENT ON COLUMN "public"."product_materials"."care_instructions" IS '保养说明';
COMMENT ON COLUMN "public"."product_materials"."cultural_significance" IS '文化意义';
COMMENT ON COLUMN "public"."product_materials"."energy_properties" IS '能量属性（针对宝石、水晶等）';
COMMENT ON COLUMN "public"."product_materials"."is_active" IS '是否激活';
COMMENT ON COLUMN "public"."product_materials"."is_featured" IS '是否推荐材质';
COMMENT ON COLUMN "public"."product_materials"."sort_order" IS '排序顺序';
COMMENT ON COLUMN "public"."product_materials"."seo_title" IS 'SEO标题';
COMMENT ON COLUMN "public"."product_materials"."seo_description" IS 'SEO描述';
COMMENT ON COLUMN "public"."product_materials"."seo_keywords" IS 'SEO关键词';

-- ----------------------------
-- Records of product_materials
-- ----------------------------

-- ----------------------------
-- Table structure for product_prices
-- ----------------------------
DROP TABLE IF EXISTS "public"."product_prices";
CREATE TABLE "public"."product_prices" (
  "id" uuid NOT NULL,
  "product_id" uuid NOT NULL,
  "currency_code" varchar(3) COLLATE "pg_catalog"."default" NOT NULL,
  "regular_price" float8 NOT NULL,
  "sale_price" float8,
  "discount_percentage" float8,
  "special_price" float8,
  "special_price_start_date" date,
  "special_price_end_date" date,
  "min_quantity" int4,
  "is_default" bool,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."product_prices"."currency_code" IS '货币代码，如USD, SGD, MYR';
COMMENT ON COLUMN "public"."product_prices"."regular_price" IS '原始价格';
COMMENT ON COLUMN "public"."product_prices"."sale_price" IS '销售价格';
COMMENT ON COLUMN "public"."product_prices"."discount_percentage" IS '折扣百分比';
COMMENT ON COLUMN "public"."product_prices"."special_price" IS '特价';
COMMENT ON COLUMN "public"."product_prices"."special_price_start_date" IS '特价开始日期';
COMMENT ON COLUMN "public"."product_prices"."special_price_end_date" IS '特价结束日期';
COMMENT ON COLUMN "public"."product_prices"."min_quantity" IS '最小购买数量';
COMMENT ON COLUMN "public"."product_prices"."is_default" IS '是否为默认币种价格';

-- ----------------------------
-- Records of product_prices
-- ----------------------------
INSERT INTO "public"."product_prices" VALUES ('7fa4e00d-d231-4aa3-bcfe-ed79b86d4770', '8412d590-9bf6-47c9-a5fc-302f1847513c', 'CNY', 1000, 880, NULL, 680, '2025-05-29', '2025-06-30', 1, 'f', '2025-05-29 07:25:23.834741', '2025-05-29 07:25:23.834741');
INSERT INTO "public"."product_prices" VALUES ('1c6139ab-d00e-422e-b5c2-d7452cd9006a', '8412d590-9bf6-47c9-a5fc-302f1847513c', 'USD', 150, 128, NULL, 100, '2025-05-29', '2025-06-30', 1, 'f', '2025-05-29 07:26:01.705558', '2025-05-29 07:26:01.705558');
INSERT INTO "public"."product_prices" VALUES ('f6095a23-2a2c-4432-9253-d222a81a8326', '4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'CNY', 1000, 880, NULL, 680, '2025-05-29', '2025-06-30', 1, 'f', '2025-06-06 00:14:00.926048', '2025-06-06 00:14:00.926048');
INSERT INTO "public"."product_prices" VALUES ('6c4ee881-eb47-4cff-b586-aa5a9286a9ae', '4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'USD', 150, 128, NULL, 100, '2025-05-29', '2025-06-30', 1, 'f', '2025-06-06 00:14:00.926574', '2025-06-06 00:14:00.926574');
INSERT INTO "public"."product_prices" VALUES ('8bf13480-5018-4a86-8aee-5dbb09057d46', 'bed054b6-14cc-43fc-98d2-00ad7d14170b', 'CNY', 1000, 880, NULL, 680, '2025-05-29', '2025-06-30', 1, 'f', '2025-06-06 00:14:00.99936', '2025-06-06 00:14:00.99936');
INSERT INTO "public"."product_prices" VALUES ('b0e2d223-5faf-4af5-b3bf-c0e6484efe0f', 'bed054b6-14cc-43fc-98d2-00ad7d14170b', 'USD', 150, 128, NULL, 100, '2025-05-29', '2025-06-30', 1, 'f', '2025-06-06 00:14:00.99936', '2025-06-06 00:14:00.99936');
INSERT INTO "public"."product_prices" VALUES ('b9b0e177-1da6-4c3e-8c38-e10f1e5988db', '10893657-5b79-4a06-852b-5b5358e447c7', 'CNY', 1000, 880, NULL, 680, '2025-05-29', '2025-06-30', 1, 'f', '2025-06-06 00:14:01.055741', '2025-06-06 00:14:01.055741');
INSERT INTO "public"."product_prices" VALUES ('76502a3a-e264-4328-9143-aae4dcd40ca7', '10893657-5b79-4a06-852b-5b5358e447c7', 'USD', 150, 128, NULL, 100, '2025-05-29', '2025-06-30', 1, 'f', '2025-06-06 00:14:01.055741', '2025-06-06 00:14:01.055741');
INSERT INTO "public"."product_prices" VALUES ('e9c42f1b-6386-4346-b0f2-944724ea13d3', 'dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'CNY', 1000, 880, NULL, 680, '2025-05-29', '2025-06-30', 1, 'f', '2025-06-06 00:14:01.111297', '2025-06-06 00:14:01.111297');
INSERT INTO "public"."product_prices" VALUES ('1f40b894-b9a5-4b16-82e4-5818bf6538e0', 'dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'USD', 150, 128, NULL, 100, '2025-05-29', '2025-06-30', 1, 'f', '2025-06-06 00:14:01.111297', '2025-06-06 00:14:01.111297');

-- ----------------------------
-- Table structure for product_scene
-- ----------------------------
DROP TABLE IF EXISTS "public"."product_scene";
CREATE TABLE "public"."product_scene" (
  "product_id" uuid NOT NULL,
  "scene_id" uuid NOT NULL
)
;

-- ----------------------------
-- Records of product_scene
-- ----------------------------

-- ----------------------------
-- Table structure for product_scenes
-- ----------------------------
DROP TABLE IF EXISTS "public"."product_scenes";
CREATE TABLE "public"."product_scenes" (
  "id" uuid NOT NULL,
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "slug" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default",
  "icon_url" varchar(255) COLLATE "pg_catalog"."default",
  "banner_url" varchar(255) COLLATE "pg_catalog"."default",
  "is_active" bool,
  "is_featured" bool,
  "sort_order" int4,
  "seo_title" varchar(255) COLLATE "pg_catalog"."default",
  "seo_description" varchar(500) COLLATE "pg_catalog"."default",
  "seo_keywords" varchar(255) COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."product_scenes"."name" IS '场景名称';
COMMENT ON COLUMN "public"."product_scenes"."slug" IS '场景别名，用于URL';
COMMENT ON COLUMN "public"."product_scenes"."description" IS '场景描述';
COMMENT ON COLUMN "public"."product_scenes"."icon_url" IS '场景图标URL';
COMMENT ON COLUMN "public"."product_scenes"."banner_url" IS '场景横幅图片URL';
COMMENT ON COLUMN "public"."product_scenes"."is_active" IS '是否激活';
COMMENT ON COLUMN "public"."product_scenes"."is_featured" IS '是否推荐场景';
COMMENT ON COLUMN "public"."product_scenes"."sort_order" IS '排序顺序';
COMMENT ON COLUMN "public"."product_scenes"."seo_title" IS 'SEO标题';
COMMENT ON COLUMN "public"."product_scenes"."seo_description" IS 'SEO描述';
COMMENT ON COLUMN "public"."product_scenes"."seo_keywords" IS 'SEO关键词';

-- ----------------------------
-- Records of product_scenes
-- ----------------------------

-- ----------------------------
-- Table structure for product_skus
-- ----------------------------
DROP TABLE IF EXISTS "public"."product_skus";
CREATE TABLE "public"."product_skus" (
  "id" uuid NOT NULL,
  "product_id" uuid NOT NULL,
  "sku_code" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "barcode" varchar(50) COLLATE "pg_catalog"."default",
  "image_url" varchar(255) COLLATE "pg_catalog"."default",
  "price_adjustment" float8,
  "weight_adjustment" float8,
  "width_adjustment" float8,
  "height_adjustment" float8,
  "length_adjustment" float8,
  "is_active" bool,
  "is_default" bool,
  "meta_data" json,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL,
  "sort_order" int4 DEFAULT 0
)
;
COMMENT ON COLUMN "public"."product_skus"."sku_code" IS 'SKU编码，唯一';
COMMENT ON COLUMN "public"."product_skus"."barcode" IS '条形码';
COMMENT ON COLUMN "public"."product_skus"."image_url" IS 'SKU特定图片URL';
COMMENT ON COLUMN "public"."product_skus"."price_adjustment" IS '相对于基础价格的调整，可正可负';
COMMENT ON COLUMN "public"."product_skus"."weight_adjustment" IS '相对于基础重量的调整，可正可负';
COMMENT ON COLUMN "public"."product_skus"."width_adjustment" IS '相对于基础宽度的调整，可正可负';
COMMENT ON COLUMN "public"."product_skus"."height_adjustment" IS '相对于基础高度的调整，可正可负';
COMMENT ON COLUMN "public"."product_skus"."length_adjustment" IS '相对于基础长度的调整，可正可负';
COMMENT ON COLUMN "public"."product_skus"."is_active" IS '是否激活';
COMMENT ON COLUMN "public"."product_skus"."is_default" IS '是否为默认SKU';
COMMENT ON COLUMN "public"."product_skus"."meta_data" IS '元数据，存储其他扩展信息';
COMMENT ON COLUMN "public"."product_skus"."sort_order" IS '排序顺序';

-- ----------------------------
-- Records of product_skus
-- ----------------------------
INSERT INTO "public"."product_skus" VALUES ('4fe91b37-7bf8-4973-8411-391175eeeb96', '8412d590-9bf6-47c9-a5fc-302f1847513c', 'SL-0001-8mm', '123456', NULL, 0, 0, 0, 0, 0, 't', 'f', 'null', '2025-05-30 05:59:52.591631', '2025-06-05 23:39:48.890754', 0);
INSERT INTO "public"."product_skus" VALUES ('55d21ca1-488e-49f1-adb7-727a491de7f8', '4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'SL-0001-8mm_COPY_1', '123456', NULL, 0, 0, 0, 0, 0, 't', 'f', 'null', '2025-06-06 00:14:00.915941', '2025-06-06 00:14:00.915941', 0);
INSERT INTO "public"."product_skus" VALUES ('c4d4aab9-825c-45c4-a182-3b7160a453da', 'bed054b6-14cc-43fc-98d2-00ad7d14170b', 'SL-0001-8mm_COPY_2', '123456', NULL, 0, 0, 0, 0, 0, 't', 'f', 'null', '2025-06-06 00:14:00.997362', '2025-06-06 00:14:00.997362', 0);
INSERT INTO "public"."product_skus" VALUES ('38ee75e2-ee3d-4447-808d-ea3048eaacb8', '10893657-5b79-4a06-852b-5b5358e447c7', 'SL-0001-8mm_COPY_3', '123456', NULL, 0, 0, 0, 0, 0, 't', 'f', 'null', '2025-06-06 00:14:01.05263', '2025-06-06 00:14:01.05263', 0);
INSERT INTO "public"."product_skus" VALUES ('6275b947-32df-4f92-851c-fb4070dcdd60', 'dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'SL-0001-8mm_COPY_4', '123456', NULL, 0, 0, 0, 0, 0, 't', 'f', 'null', '2025-06-06 00:14:01.108298', '2025-06-06 00:14:01.108298', 0);

-- ----------------------------
-- Table structure for product_symbol
-- ----------------------------
DROP TABLE IF EXISTS "public"."product_symbol";
CREATE TABLE "public"."product_symbol" (
  "product_id" uuid NOT NULL,
  "symbol_id" uuid NOT NULL
)
;

-- ----------------------------
-- Records of product_symbol
-- ----------------------------

-- ----------------------------
-- Table structure for product_symbols
-- ----------------------------
DROP TABLE IF EXISTS "public"."product_symbols";
CREATE TABLE "public"."product_symbols" (
  "id" uuid NOT NULL,
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "slug" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default",
  "icon_url" varchar(255) COLLATE "pg_catalog"."default",
  "image_url" varchar(255) COLLATE "pg_catalog"."default",
  "cultural_meaning" text COLLATE "pg_catalog"."default",
  "spiritual_significance" text COLLATE "pg_catalog"."default",
  "origin" text COLLATE "pg_catalog"."default",
  "usage_guide" text COLLATE "pg_catalog"."default",
  "is_active" bool,
  "is_featured" bool,
  "sort_order" int4,
  "seo_title" varchar(255) COLLATE "pg_catalog"."default",
  "seo_description" varchar(500) COLLATE "pg_catalog"."default",
  "seo_keywords" varchar(255) COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."product_symbols"."name" IS '符号名称';
COMMENT ON COLUMN "public"."product_symbols"."slug" IS '符号别名，用于URL';
COMMENT ON COLUMN "public"."product_symbols"."description" IS '符号描述';
COMMENT ON COLUMN "public"."product_symbols"."icon_url" IS '符号图标URL';
COMMENT ON COLUMN "public"."product_symbols"."image_url" IS '符号图片URL';
COMMENT ON COLUMN "public"."product_symbols"."cultural_meaning" IS '文化含义';
COMMENT ON COLUMN "public"."product_symbols"."spiritual_significance" IS '精神意义';
COMMENT ON COLUMN "public"."product_symbols"."origin" IS '起源和历史';
COMMENT ON COLUMN "public"."product_symbols"."usage_guide" IS '使用指南';
COMMENT ON COLUMN "public"."product_symbols"."is_active" IS '是否激活';
COMMENT ON COLUMN "public"."product_symbols"."is_featured" IS '是否推荐符号';
COMMENT ON COLUMN "public"."product_symbols"."sort_order" IS '排序顺序';
COMMENT ON COLUMN "public"."product_symbols"."seo_title" IS 'SEO标题';
COMMENT ON COLUMN "public"."product_symbols"."seo_description" IS 'SEO描述';
COMMENT ON COLUMN "public"."product_symbols"."seo_keywords" IS 'SEO关键词';

-- ----------------------------
-- Records of product_symbols
-- ----------------------------

-- ----------------------------
-- Table structure for product_tag
-- ----------------------------
DROP TABLE IF EXISTS "public"."product_tag";
CREATE TABLE "public"."product_tag" (
  "product_id" uuid NOT NULL,
  "tag_id" uuid NOT NULL
)
;

-- ----------------------------
-- Records of product_tag
-- ----------------------------

-- ----------------------------
-- Table structure for product_tags
-- ----------------------------
DROP TABLE IF EXISTS "public"."product_tags";
CREATE TABLE "public"."product_tags" (
  "id" uuid NOT NULL,
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "slug" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default",
  "icon_url" varchar(255) COLLATE "pg_catalog"."default",
  "color" varchar(30) COLLATE "pg_catalog"."default",
  "is_active" bool,
  "sort_order" int4,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."product_tags"."name" IS '标签名称';
COMMENT ON COLUMN "public"."product_tags"."slug" IS '标签别名，用于URL';
COMMENT ON COLUMN "public"."product_tags"."description" IS '标签描述';
COMMENT ON COLUMN "public"."product_tags"."icon_url" IS '标签图标URL';
COMMENT ON COLUMN "public"."product_tags"."color" IS '标签颜色代码，如#FF5733';
COMMENT ON COLUMN "public"."product_tags"."is_active" IS '是否激活';
COMMENT ON COLUMN "public"."product_tags"."sort_order" IS '排序顺序';

-- ----------------------------
-- Records of product_tags
-- ----------------------------

-- ----------------------------
-- Table structure for product_target_group
-- ----------------------------
DROP TABLE IF EXISTS "public"."product_target_group";
CREATE TABLE "public"."product_target_group" (
  "product_id" uuid NOT NULL,
  "target_group_id" uuid NOT NULL
)
;

-- ----------------------------
-- Records of product_target_group
-- ----------------------------

-- ----------------------------
-- Table structure for product_target_groups
-- ----------------------------
DROP TABLE IF EXISTS "public"."product_target_groups";
CREATE TABLE "public"."product_target_groups" (
  "id" uuid NOT NULL,
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "slug" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default",
  "icon_url" varchar(255) COLLATE "pg_catalog"."default",
  "gender" "public"."gendertype",
  "age_group" "public"."agegroup",
  "is_couple" bool,
  "is_family" bool,
  "is_active" bool,
  "is_featured" bool,
  "sort_order" int4,
  "buying_preferences" text COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."product_target_groups"."name" IS '目标人群名称';
COMMENT ON COLUMN "public"."product_target_groups"."slug" IS '目标人群别名，用于URL';
COMMENT ON COLUMN "public"."product_target_groups"."description" IS '目标人群描述';
COMMENT ON COLUMN "public"."product_target_groups"."icon_url" IS '目标人群图标URL';
COMMENT ON COLUMN "public"."product_target_groups"."gender" IS '性别类型';
COMMENT ON COLUMN "public"."product_target_groups"."age_group" IS '年龄段';
COMMENT ON COLUMN "public"."product_target_groups"."is_couple" IS '是否情侣/伴侣群体';
COMMENT ON COLUMN "public"."product_target_groups"."is_family" IS '是否家庭群体';
COMMENT ON COLUMN "public"."product_target_groups"."is_active" IS '是否激活';
COMMENT ON COLUMN "public"."product_target_groups"."is_featured" IS '是否推荐目标人群';
COMMENT ON COLUMN "public"."product_target_groups"."sort_order" IS '排序顺序';
COMMENT ON COLUMN "public"."product_target_groups"."buying_preferences" IS '购买偏好';

-- ----------------------------
-- Records of product_target_groups
-- ----------------------------

-- ----------------------------
-- Table structure for product_theme
-- ----------------------------
DROP TABLE IF EXISTS "public"."product_theme";
CREATE TABLE "public"."product_theme" (
  "product_id" uuid NOT NULL,
  "theme_id" uuid NOT NULL
)
;

-- ----------------------------
-- Records of product_theme
-- ----------------------------

-- ----------------------------
-- Table structure for product_themes
-- ----------------------------
DROP TABLE IF EXISTS "public"."product_themes";
CREATE TABLE "public"."product_themes" (
  "id" uuid NOT NULL,
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "slug" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default",
  "icon_url" varchar(255) COLLATE "pg_catalog"."default",
  "banner_url" varchar(255) COLLATE "pg_catalog"."default",
  "background_color" varchar(30) COLLATE "pg_catalog"."default",
  "text_color" varchar(30) COLLATE "pg_catalog"."default",
  "start_date" date,
  "end_date" date,
  "is_seasonal" bool,
  "is_cultural" bool,
  "is_yearly" bool,
  "is_active" bool,
  "is_featured" bool,
  "sort_order" int4,
  "seo_title" varchar(255) COLLATE "pg_catalog"."default",
  "seo_description" varchar(500) COLLATE "pg_catalog"."default",
  "seo_keywords" varchar(255) COLLATE "pg_catalog"."default",
  "cultural_significance" text COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."product_themes"."name" IS '主题名称';
COMMENT ON COLUMN "public"."product_themes"."slug" IS '主题别名，用于URL';
COMMENT ON COLUMN "public"."product_themes"."description" IS '主题描述';
COMMENT ON COLUMN "public"."product_themes"."icon_url" IS '主题图标URL';
COMMENT ON COLUMN "public"."product_themes"."banner_url" IS '主题横幅图片URL';
COMMENT ON COLUMN "public"."product_themes"."background_color" IS '主题背景颜色代码';
COMMENT ON COLUMN "public"."product_themes"."text_color" IS '主题文本颜色代码';
COMMENT ON COLUMN "public"."product_themes"."start_date" IS '主题开始日期';
COMMENT ON COLUMN "public"."product_themes"."end_date" IS '主题结束日期';
COMMENT ON COLUMN "public"."product_themes"."is_seasonal" IS '是否季节性主题';
COMMENT ON COLUMN "public"."product_themes"."is_cultural" IS '是否文化相关主题';
COMMENT ON COLUMN "public"."product_themes"."is_yearly" IS '是否年度主题';
COMMENT ON COLUMN "public"."product_themes"."is_active" IS '是否激活';
COMMENT ON COLUMN "public"."product_themes"."is_featured" IS '是否推荐主题';
COMMENT ON COLUMN "public"."product_themes"."sort_order" IS '排序顺序';
COMMENT ON COLUMN "public"."product_themes"."seo_title" IS 'SEO标题';
COMMENT ON COLUMN "public"."product_themes"."seo_description" IS 'SEO描述';
COMMENT ON COLUMN "public"."product_themes"."seo_keywords" IS 'SEO关键词';
COMMENT ON COLUMN "public"."product_themes"."cultural_significance" IS '文化意义';

-- ----------------------------
-- Records of product_themes
-- ----------------------------

-- ----------------------------
-- Table structure for product_translations
-- ----------------------------
DROP TABLE IF EXISTS "public"."product_translations";
CREATE TABLE "public"."product_translations" (
  "id" uuid NOT NULL,
  "product_id" uuid NOT NULL,
  "language_code" varchar(10) COLLATE "pg_catalog"."default" NOT NULL,
  "name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "short_description" text COLLATE "pg_catalog"."default",
  "description" text COLLATE "pg_catalog"."default",
  "specifications" text COLLATE "pg_catalog"."default",
  "benefits" text COLLATE "pg_catalog"."default",
  "instructions" text COLLATE "pg_catalog"."default",
  "seo_title" varchar(255) COLLATE "pg_catalog"."default",
  "seo_description" varchar(500) COLLATE "pg_catalog"."default",
  "seo_keywords" varchar(255) COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."product_translations"."language_code" IS '语言代码，如en-US, zh-CN';
COMMENT ON COLUMN "public"."product_translations"."name" IS '商品名称';
COMMENT ON COLUMN "public"."product_translations"."short_description" IS '商品简短描述';
COMMENT ON COLUMN "public"."product_translations"."description" IS '商品详细描述';
COMMENT ON COLUMN "public"."product_translations"."specifications" IS '商品规格';
COMMENT ON COLUMN "public"."product_translations"."benefits" IS '商品好处/特点';
COMMENT ON COLUMN "public"."product_translations"."instructions" IS '使用说明';
COMMENT ON COLUMN "public"."product_translations"."seo_title" IS 'SEO标题';
COMMENT ON COLUMN "public"."product_translations"."seo_description" IS 'SEO描述';
COMMENT ON COLUMN "public"."product_translations"."seo_keywords" IS 'SEO关键词';

-- ----------------------------
-- Records of product_translations
-- ----------------------------
INSERT INTO "public"."product_translations" VALUES ('041c89ba-a66b-464d-b590-9f92bc0069c2', '2304e61a-ce9a-48a2-94bf-bdacda1ed1de', 'zh-CN', '玉石吊坠', '玉石吊坠', '玉石吊坠', NULL, NULL, NULL, NULL, NULL, NULL, '2025-05-28 05:26:01.204445', '2025-05-28 05:26:01.204445');
INSERT INTO "public"."product_translations" VALUES ('e2630eba-eedd-4058-9fab-84c86e4fe011', 'bad5392d-9231-4c72-82b9-2b61a40e53d5', 'zh-CN', '龙形项链', NULL, '龙形项链', NULL, NULL, NULL, NULL, NULL, NULL, '2025-05-28 06:26:14.786735', '2025-05-28 06:26:14.786735');
INSERT INTO "public"."product_translations" VALUES ('9d01e085-baa8-4cd5-82bb-fb2df0b4a1f9', '8412d590-9bf6-47c9-a5fc-302f1847513c', 'zh-cn', '五花手链', '以梵克雅宝Lucky Spring系列为灵感蓝本，融合西班牙阿尔罕布拉宫建筑纹样与东方自然元素', '五朵立体雕刻花卉（如四叶草、梅花、铃兰）以黄金分割比例串联，寓意“五重幸运守护”，花瓣镶嵌红玉髓、珍珠母贝、孔雀石等天然宝石，通过0.03mm钻石刀头微雕工艺呈现细腻纹路。链节间采用“三点悬浮系统”，内置航天级润滑剂，可承受10万次开合磨损。', '标准链长18.5cm（无调节扣，适配14-18cm腕围），定制款可选15.5-21.5cm', '文化价值​：四叶草符号传承千年凯尔特文明，融合伊斯兰建筑美学，兼具博物馆级艺术性与日常佩戴场景', '先化妆喷香水，最后佩戴手链', '梵克雅宝同款天然宝石五花手链女18K金幸运四叶草轻奢手饰', '手工捶揲18K金五花手链，镶嵌南太平洋珍珠母贝+巴西红玉髓，以西班牙阿尔罕布拉宫黄金比例串联五重幸运符号。适配职场通勤/宴会晚装，磁吸搭扣经10万次开合测试，赠送定制防氧化礼盒', '五花手链、四叶草手链、招财手链、18K金手链', '2025-05-29 08:22:10.138524', '2025-05-29 08:22:10.138524');
INSERT INTO "public"."product_translations" VALUES ('d63ed2d6-01f3-47b0-861b-b4ba3eb7d2f1', '8412d590-9bf6-47c9-a5fc-302f1847513c', 'en-us', 'Five-Flower Bracelet', 'Inspired by Van Cleef & Arpels'' Lucky Spring collection, blending the architectural motifs of Spain''s Alhambra Palace with Eastern natural elements', 'Five three-dimensionally carved flowers (such as four-leaf clovers, plum blossoms, and lilies of the valley) are connected in golden ratio proportions, symbolizing ''Fivefold Luck Protection.'' The petals are inlaid with natural gemstones like carnelian, mother-of-pearl, and malachite, showcasing intricate details through 0.03mm diamond-tip micro-carving. The links feature a ''Three-Point Suspension System'' with aerospace-grade lubricant, capable of withstanding 100,000 open-close cycles.', 'Standard chain length: 18.5cm (non-adjustable, fits 14-18cm wrist circumference). Custom lengths available: 15.5-21.5cm.', 'Cultural Value: The four-leaf clover motif carries millennia of Celtic heritage, fused with Islamic architectural aesthetics, offering museum-grade artistry suitable for daily wear.', 'Apply makeup and perfume first, then wear the bracelet.', 'Van Cleef & Arpels-Inspired Five-Flower Bracelet for Women with Natural Gemstones, 18K Gold Lucky Four-Leaf Clover Luxury Jewelry', 'Hand-hammered 18K gold five-flower bracelet featuring South Pacific mother-of-pearl and Brazilian carnelian inlays, connecting five lucky symbols in Alhambra Palace''s golden ratio. Perfect for office wear or evening events, with magnetic clasp tested for 100,000 cycles. Includes custom anti-tarnish gift box.', 'five-flower bracelet, four-leaf clover bracelet, wealth-attracting bracelet, 18K gold bracelet', '2025-05-29 08:33:52.139664', '2025-05-29 08:33:52.139664');
INSERT INTO "public"."product_translations" VALUES ('70c4d166-38c7-4ad5-bcd6-f8d5567f8166', '8412d590-9bf6-47c9-a5fc-302f1847513c', 'ja-jp', '五華ブレスレット', 'ヴァン クリーフ＆アーペルのラッキースプリングコレクションをインスピレーションとし、スペインのアルハンブラ宮殿の建築模様と東洋の自然要素を融合させたデザイン', '立体彫刻された5つの花（クローバー、梅の花、スズランなど）が黄金比で連なり、「五重の幸運の守り」を意味します。花びらにはカーネリアン、パール母貝、マラカイトなどの天然石が埋め込まれ、0.03mmのダイヤモンドビットによる微細な彫刻技術で繊細な模様を表現。チェーン連結部には「三点浮遊システム」を採用し、航空宇宙級潤滑剤を内蔵、10万回の開閉に耐える耐久性を実現。', '標準チェーン長18.5cm（調節金具なし、14-18cmの手首周りに適合）、オーダーメイド版は15.5-21.5cmから選択可能', '文化的価値：クローバーシンボルは千年のケルト文明を継承し、イスラム建築美学と融合、博物館級の芸術性と日常着用シーンを兼ね備えています', '化粧と香水を付けた後、最後にブレスレットを着用してください', 'ヴァン クリーフ＆アーペル風天然石五華ブレスレット 18Kゴールド ラッキークローバー レディース軽奢華アクセサリー', '手打ち18Kゴールド製五華ブレスレット。南太平洋産パール母貝+ブラジル産カーネリアンを埋め込み、スペイン・アルハンブラ宮殿の黄金比で五つの幸運シンボルを連結。ビジネス通勤/パーティー夜会に適応、マグネットクラスプは10万回開閉テスト済み。特製酸化防止ギフトボックス付属', '五華ブレスレット, クローバーブレスレット, 開運ブレスレット, 18Kゴールドブレスレット', '2025-05-29 08:35:42.394906', '2025-05-29 08:35:42.394906');
INSERT INTO "public"."product_translations" VALUES ('74397e25-66b2-4485-a6e3-32cf958d66ce', '8412d590-9bf6-47c9-a5fc-302f1847513c', 'th-th', 'สร้อยข้อมือดอกไม้ 5 ดอก', 'ได้รับแรงบันดาลใจจากคอลเลกชัน Lucky Spring ของ Van Cleef & Arpels ผสมผสานลวดลายสถาปัตยกรรมจาก Alhambra Palace ของสเปนกับองค์ประกอบธรรมชาติแบบตะวันออก', 'ดอกไม้ 5 ดอก (เช่นใบโคลเวอร์, ดอกพลัม, ลิลลี่แห่งหุบเขา) ที่แกะสลักสามมิติเรียงกันตามสัดส่วนทองคำ แสดงถึง "การปกป้องแห่งโชคลาภ 5 ประการ" กลีบดอกไม้ประดับด้วยหินธรรมชาติเช่นคาร์เนเลียน, มุก, และมรกต โดยใช้เทคนิคการแกะสลักละเอียดด้วยหัวเพชร 0.03mm ข้อต่อสร้อยใช้ "ระบบแขวน 3 จุด" ที่มีสารหล่อลื่นระดับการบินและอวกาศภายใน ทนทานต่อการเปิด-ปิดได้ถึง 100,000 ครั้ง', 'ความยาวมาตรฐาน 18.5 ซม. (ไม่มีตัวปรับความยาว เหมาะกับเส้นรอบวงข้อมือ 14-18 ซม.) แบบสั่งทำพิเศษสามารถเลือกความยาวได้ตั้งแต่ 15.5-21.5 ซม.', 'คุณค่าทางวัฒนธรรม: สัญลักษณ์ใบโคลเวอร์สืบทอดอารยธรรมเซลติกที่มีอายุพันปี ผสมผสานกับสุนทรียศาสตร์สถาปัตยกรรมอิสลาม มีทั้งคุณค่าทางศิลปะระดับพิพิธภัณฑ์และเหมาะกับการสวมใส่ในชีวิตประจำวัน', 'แต่งหน้าและฉีดน้ำหอมก่อน แล้วจึงสวมสร้อยข้อมือ', 'สร้อยข้อมือดอกไม้ 5 ดอกสำหรับผู้หญิง แบบเดียวกับ Van Cleef & Arpels ทำจากทอง 18K พร้อมหินธรรมชาติ ใบโคลเวอร์นำโชค เครื่องประดับแฟชั่นสุดหรู', 'สร้อยข้อมือดอกไม้ 5 ดอกทำจากทอง 18K ตอกมือ ประดับด้วยมุกจากแปซิฟิกใต้และคาร์เนเลียนจากบราซิล เรียงกันตามสัดส่วนทองคำของ Alhambra Palace แสดงถึงสัญลักษณ์โชคลาภ 5 ประการ เหมาะสำหรับการทำงานหรืองานเลี้ยง มีตัวล็อกแม่เหล็กที่ผ่านการทดสอบการเปิด-ปิด 100,000 ครั้ง พร้อมกล่องของขวัญป้องกันการออกซิไดซ์', 'สร้อยข้อมือดอกไม้ 5 ดอก, สร้อยข้อมือใบโคลเวอร์, สร้อยข้อมือนำโชค, สร้อยข้อมือทอง 18K', '2025-05-29 08:37:33.125364', '2025-05-29 08:37:33.125364');
INSERT INTO "public"."product_translations" VALUES ('0f4b2f5a-85a5-493a-8ca3-da723e5d36d2', '4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'zh-cn', '五花手链 (副本1)', '以梵克雅宝Lucky Spring系列为灵感蓝本，融合西班牙阿尔罕布拉宫建筑纹样与东方自然元素', '五朵立体雕刻花卉（如四叶草、梅花、铃兰）以黄金分割比例串联，寓意“五重幸运守护”，花瓣镶嵌红玉髓、珍珠母贝、孔雀石等天然宝石，通过0.03mm钻石刀头微雕工艺呈现细腻纹路。链节间采用“三点悬浮系统”，内置航天级润滑剂，可承受10万次开合磨损。', '标准链长18.5cm（无调节扣，适配14-18cm腕围），定制款可选15.5-21.5cm', '文化价值​：四叶草符号传承千年凯尔特文明，融合伊斯兰建筑美学，兼具博物馆级艺术性与日常佩戴场景', '先化妆喷香水，最后佩戴手链', '梵克雅宝同款天然宝石五花手链女18K金幸运四叶草轻奢手饰', '手工捶揲18K金五花手链，镶嵌南太平洋珍珠母贝+巴西红玉髓，以西班牙阿尔罕布拉宫黄金比例串联五重幸运符号。适配职场通勤/宴会晚装，磁吸搭扣经10万次开合测试，赠送定制防氧化礼盒', '五花手链、四叶草手链、招财手链、18K金手链', '2025-06-06 00:14:00.926048', '2025-06-06 00:14:00.926048');
INSERT INTO "public"."product_translations" VALUES ('79890a2c-a63b-4d34-9a5a-260be0ef79e4', '4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'en-us', 'Five-Flower Bracelet (副本1)', 'Inspired by Van Cleef & Arpels'' Lucky Spring collection, blending the architectural motifs of Spain''s Alhambra Palace with Eastern natural elements', 'Five three-dimensionally carved flowers (such as four-leaf clovers, plum blossoms, and lilies of the valley) are connected in golden ratio proportions, symbolizing ''Fivefold Luck Protection.'' The petals are inlaid with natural gemstones like carnelian, mother-of-pearl, and malachite, showcasing intricate details through 0.03mm diamond-tip micro-carving. The links feature a ''Three-Point Suspension System'' with aerospace-grade lubricant, capable of withstanding 100,000 open-close cycles.', 'Standard chain length: 18.5cm (non-adjustable, fits 14-18cm wrist circumference). Custom lengths available: 15.5-21.5cm.', 'Cultural Value: The four-leaf clover motif carries millennia of Celtic heritage, fused with Islamic architectural aesthetics, offering museum-grade artistry suitable for daily wear.', 'Apply makeup and perfume first, then wear the bracelet.', 'Van Cleef & Arpels-Inspired Five-Flower Bracelet for Women with Natural Gemstones, 18K Gold Lucky Four-Leaf Clover Luxury Jewelry', 'Hand-hammered 18K gold five-flower bracelet featuring South Pacific mother-of-pearl and Brazilian carnelian inlays, connecting five lucky symbols in Alhambra Palace''s golden ratio. Perfect for office wear or evening events, with magnetic clasp tested for 100,000 cycles. Includes custom anti-tarnish gift box.', 'five-flower bracelet, four-leaf clover bracelet, wealth-attracting bracelet, 18K gold bracelet', '2025-06-06 00:14:00.926048', '2025-06-06 00:14:00.926048');
INSERT INTO "public"."product_translations" VALUES ('3acef337-14ac-49f6-8808-18112d3b6814', '4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'ja-jp', '五華ブレスレット (副本1)', 'ヴァン クリーフ＆アーペルのラッキースプリングコレクションをインスピレーションとし、スペインのアルハンブラ宮殿の建築模様と東洋の自然要素を融合させたデザイン', '立体彫刻された5つの花（クローバー、梅の花、スズランなど）が黄金比で連なり、「五重の幸運の守り」を意味します。花びらにはカーネリアン、パール母貝、マラカイトなどの天然石が埋め込まれ、0.03mmのダイヤモンドビットによる微細な彫刻技術で繊細な模様を表現。チェーン連結部には「三点浮遊システム」を採用し、航空宇宙級潤滑剤を内蔵、10万回の開閉に耐える耐久性を実現。', '標準チェーン長18.5cm（調節金具なし、14-18cmの手首周りに適合）、オーダーメイド版は15.5-21.5cmから選択可能', '文化的価値：クローバーシンボルは千年のケルト文明を継承し、イスラム建築美学と融合、博物館級の芸術性と日常着用シーンを兼ね備えています', '化粧と香水を付けた後、最後にブレスレットを着用してください', 'ヴァン クリーフ＆アーペル風天然石五華ブレスレット 18Kゴールド ラッキークローバー レディース軽奢華アクセサリー', '手打ち18Kゴールド製五華ブレスレット。南太平洋産パール母貝+ブラジル産カーネリアンを埋め込み、スペイン・アルハンブラ宮殿の黄金比で五つの幸運シンボルを連結。ビジネス通勤/パーティー夜会に適応、マグネットクラスプは10万回開閉テスト済み。特製酸化防止ギフトボックス付属', '五華ブレスレット, クローバーブレスレット, 開運ブレスレット, 18Kゴールドブレスレット', '2025-06-06 00:14:00.926048', '2025-06-06 00:14:00.926048');
INSERT INTO "public"."product_translations" VALUES ('b92b9c30-49c3-4a7d-a564-909fa830d5ac', '4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'th-th', 'สร้อยข้อมือดอกไม้ 5 ดอก (副本1)', 'ได้รับแรงบันดาลใจจากคอลเลกชัน Lucky Spring ของ Van Cleef & Arpels ผสมผสานลวดลายสถาปัตยกรรมจาก Alhambra Palace ของสเปนกับองค์ประกอบธรรมชาติแบบตะวันออก', 'ดอกไม้ 5 ดอก (เช่นใบโคลเวอร์, ดอกพลัม, ลิลลี่แห่งหุบเขา) ที่แกะสลักสามมิติเรียงกันตามสัดส่วนทองคำ แสดงถึง "การปกป้องแห่งโชคลาภ 5 ประการ" กลีบดอกไม้ประดับด้วยหินธรรมชาติเช่นคาร์เนเลียน, มุก, และมรกต โดยใช้เทคนิคการแกะสลักละเอียดด้วยหัวเพชร 0.03mm ข้อต่อสร้อยใช้ "ระบบแขวน 3 จุด" ที่มีสารหล่อลื่นระดับการบินและอวกาศภายใน ทนทานต่อการเปิด-ปิดได้ถึง 100,000 ครั้ง', 'ความยาวมาตรฐาน 18.5 ซม. (ไม่มีตัวปรับความยาว เหมาะกับเส้นรอบวงข้อมือ 14-18 ซม.) แบบสั่งทำพิเศษสามารถเลือกความยาวได้ตั้งแต่ 15.5-21.5 ซม.', 'คุณค่าทางวัฒนธรรม: สัญลักษณ์ใบโคลเวอร์สืบทอดอารยธรรมเซลติกที่มีอายุพันปี ผสมผสานกับสุนทรียศาสตร์สถาปัตยกรรมอิสลาม มีทั้งคุณค่าทางศิลปะระดับพิพิธภัณฑ์และเหมาะกับการสวมใส่ในชีวิตประจำวัน', 'แต่งหน้าและฉีดน้ำหอมก่อน แล้วจึงสวมสร้อยข้อมือ', 'สร้อยข้อมือดอกไม้ 5 ดอกสำหรับผู้หญิง แบบเดียวกับ Van Cleef & Arpels ทำจากทอง 18K พร้อมหินธรรมชาติ ใบโคลเวอร์นำโชค เครื่องประดับแฟชั่นสุดหรู', 'สร้อยข้อมือดอกไม้ 5 ดอกทำจากทอง 18K ตอกมือ ประดับด้วยมุกจากแปซิฟิกใต้และคาร์เนเลียนจากบราซิล เรียงกันตามสัดส่วนทองคำของ Alhambra Palace แสดงถึงสัญลักษณ์โชคลาภ 5 ประการ เหมาะสำหรับการทำงานหรืองานเลี้ยง มีตัวล็อกแม่เหล็กที่ผ่านการทดสอบการเปิด-ปิด 100,000 ครั้ง พร้อมกล่องของขวัญป้องกันการออกซิไดซ์', 'สร้อยข้อมือดอกไม้ 5 ดอก, สร้อยข้อมือใบโคลเวอร์, สร้อยข้อมือนำโชค, สร้อยข้อมือทอง 18K', '2025-06-06 00:14:00.926048', '2025-06-06 00:14:00.926048');
INSERT INTO "public"."product_translations" VALUES ('e4147210-a16b-4341-97bc-814d4f081969', 'bed054b6-14cc-43fc-98d2-00ad7d14170b', 'zh-cn', '五花手链 (副本2)', '以梵克雅宝Lucky Spring系列为灵感蓝本，融合西班牙阿尔罕布拉宫建筑纹样与东方自然元素', '五朵立体雕刻花卉（如四叶草、梅花、铃兰）以黄金分割比例串联，寓意“五重幸运守护”，花瓣镶嵌红玉髓、珍珠母贝、孔雀石等天然宝石，通过0.03mm钻石刀头微雕工艺呈现细腻纹路。链节间采用“三点悬浮系统”，内置航天级润滑剂，可承受10万次开合磨损。', '标准链长18.5cm（无调节扣，适配14-18cm腕围），定制款可选15.5-21.5cm', '文化价值​：四叶草符号传承千年凯尔特文明，融合伊斯兰建筑美学，兼具博物馆级艺术性与日常佩戴场景', '先化妆喷香水，最后佩戴手链', '梵克雅宝同款天然宝石五花手链女18K金幸运四叶草轻奢手饰', '手工捶揲18K金五花手链，镶嵌南太平洋珍珠母贝+巴西红玉髓，以西班牙阿尔罕布拉宫黄金比例串联五重幸运符号。适配职场通勤/宴会晚装，磁吸搭扣经10万次开合测试，赠送定制防氧化礼盒', '五花手链、四叶草手链、招财手链、18K金手链', '2025-06-06 00:14:00.99936', '2025-06-06 00:14:00.99936');
INSERT INTO "public"."product_translations" VALUES ('a68234f1-8a91-4d59-a231-4405313b723f', 'bed054b6-14cc-43fc-98d2-00ad7d14170b', 'en-us', 'Five-Flower Bracelet (副本2)', 'Inspired by Van Cleef & Arpels'' Lucky Spring collection, blending the architectural motifs of Spain''s Alhambra Palace with Eastern natural elements', 'Five three-dimensionally carved flowers (such as four-leaf clovers, plum blossoms, and lilies of the valley) are connected in golden ratio proportions, symbolizing ''Fivefold Luck Protection.'' The petals are inlaid with natural gemstones like carnelian, mother-of-pearl, and malachite, showcasing intricate details through 0.03mm diamond-tip micro-carving. The links feature a ''Three-Point Suspension System'' with aerospace-grade lubricant, capable of withstanding 100,000 open-close cycles.', 'Standard chain length: 18.5cm (non-adjustable, fits 14-18cm wrist circumference). Custom lengths available: 15.5-21.5cm.', 'Cultural Value: The four-leaf clover motif carries millennia of Celtic heritage, fused with Islamic architectural aesthetics, offering museum-grade artistry suitable for daily wear.', 'Apply makeup and perfume first, then wear the bracelet.', 'Van Cleef & Arpels-Inspired Five-Flower Bracelet for Women with Natural Gemstones, 18K Gold Lucky Four-Leaf Clover Luxury Jewelry', 'Hand-hammered 18K gold five-flower bracelet featuring South Pacific mother-of-pearl and Brazilian carnelian inlays, connecting five lucky symbols in Alhambra Palace''s golden ratio. Perfect for office wear or evening events, with magnetic clasp tested for 100,000 cycles. Includes custom anti-tarnish gift box.', 'five-flower bracelet, four-leaf clover bracelet, wealth-attracting bracelet, 18K gold bracelet', '2025-06-06 00:14:00.99936', '2025-06-06 00:14:00.99936');
INSERT INTO "public"."product_translations" VALUES ('4e01adf7-913c-482b-94a4-33cc6363fc21', 'bed054b6-14cc-43fc-98d2-00ad7d14170b', 'ja-jp', '五華ブレスレット (副本2)', 'ヴァン クリーフ＆アーペルのラッキースプリングコレクションをインスピレーションとし、スペインのアルハンブラ宮殿の建築模様と東洋の自然要素を融合させたデザイン', '立体彫刻された5つの花（クローバー、梅の花、スズランなど）が黄金比で連なり、「五重の幸運の守り」を意味します。花びらにはカーネリアン、パール母貝、マラカイトなどの天然石が埋め込まれ、0.03mmのダイヤモンドビットによる微細な彫刻技術で繊細な模様を表現。チェーン連結部には「三点浮遊システム」を採用し、航空宇宙級潤滑剤を内蔵、10万回の開閉に耐える耐久性を実現。', '標準チェーン長18.5cm（調節金具なし、14-18cmの手首周りに適合）、オーダーメイド版は15.5-21.5cmから選択可能', '文化的価値：クローバーシンボルは千年のケルト文明を継承し、イスラム建築美学と融合、博物館級の芸術性と日常着用シーンを兼ね備えています', '化粧と香水を付けた後、最後にブレスレットを着用してください', 'ヴァン クリーフ＆アーペル風天然石五華ブレスレット 18Kゴールド ラッキークローバー レディース軽奢華アクセサリー', '手打ち18Kゴールド製五華ブレスレット。南太平洋産パール母貝+ブラジル産カーネリアンを埋め込み、スペイン・アルハンブラ宮殿の黄金比で五つの幸運シンボルを連結。ビジネス通勤/パーティー夜会に適応、マグネットクラスプは10万回開閉テスト済み。特製酸化防止ギフトボックス付属', '五華ブレスレット, クローバーブレスレット, 開運ブレスレット, 18Kゴールドブレスレット', '2025-06-06 00:14:00.99936', '2025-06-06 00:14:00.99936');
INSERT INTO "public"."product_translations" VALUES ('1466b328-7a20-4d4b-8103-1c2613d32f10', 'bed054b6-14cc-43fc-98d2-00ad7d14170b', 'th-th', 'สร้อยข้อมือดอกไม้ 5 ดอก (副本2)', 'ได้รับแรงบันดาลใจจากคอลเลกชัน Lucky Spring ของ Van Cleef & Arpels ผสมผสานลวดลายสถาปัตยกรรมจาก Alhambra Palace ของสเปนกับองค์ประกอบธรรมชาติแบบตะวันออก', 'ดอกไม้ 5 ดอก (เช่นใบโคลเวอร์, ดอกพลัม, ลิลลี่แห่งหุบเขา) ที่แกะสลักสามมิติเรียงกันตามสัดส่วนทองคำ แสดงถึง "การปกป้องแห่งโชคลาภ 5 ประการ" กลีบดอกไม้ประดับด้วยหินธรรมชาติเช่นคาร์เนเลียน, มุก, และมรกต โดยใช้เทคนิคการแกะสลักละเอียดด้วยหัวเพชร 0.03mm ข้อต่อสร้อยใช้ "ระบบแขวน 3 จุด" ที่มีสารหล่อลื่นระดับการบินและอวกาศภายใน ทนทานต่อการเปิด-ปิดได้ถึง 100,000 ครั้ง', 'ความยาวมาตรฐาน 18.5 ซม. (ไม่มีตัวปรับความยาว เหมาะกับเส้นรอบวงข้อมือ 14-18 ซม.) แบบสั่งทำพิเศษสามารถเลือกความยาวได้ตั้งแต่ 15.5-21.5 ซม.', 'คุณค่าทางวัฒนธรรม: สัญลักษณ์ใบโคลเวอร์สืบทอดอารยธรรมเซลติกที่มีอายุพันปี ผสมผสานกับสุนทรียศาสตร์สถาปัตยกรรมอิสลาม มีทั้งคุณค่าทางศิลปะระดับพิพิธภัณฑ์และเหมาะกับการสวมใส่ในชีวิตประจำวัน', 'แต่งหน้าและฉีดน้ำหอมก่อน แล้วจึงสวมสร้อยข้อมือ', 'สร้อยข้อมือดอกไม้ 5 ดอกสำหรับผู้หญิง แบบเดียวกับ Van Cleef & Arpels ทำจากทอง 18K พร้อมหินธรรมชาติ ใบโคลเวอร์นำโชค เครื่องประดับแฟชั่นสุดหรู', 'สร้อยข้อมือดอกไม้ 5 ดอกทำจากทอง 18K ตอกมือ ประดับด้วยมุกจากแปซิฟิกใต้และคาร์เนเลียนจากบราซิล เรียงกันตามสัดส่วนทองคำของ Alhambra Palace แสดงถึงสัญลักษณ์โชคลาภ 5 ประการ เหมาะสำหรับการทำงานหรืองานเลี้ยง มีตัวล็อกแม่เหล็กที่ผ่านการทดสอบการเปิด-ปิด 100,000 ครั้ง พร้อมกล่องของขวัญป้องกันการออกซิไดซ์', 'สร้อยข้อมือดอกไม้ 5 ดอก, สร้อยข้อมือใบโคลเวอร์, สร้อยข้อมือนำโชค, สร้อยข้อมือทอง 18K', '2025-06-06 00:14:00.99936', '2025-06-06 00:14:00.99936');
INSERT INTO "public"."product_translations" VALUES ('0f0dc84e-b469-4f6a-b804-111aa7887de6', '10893657-5b79-4a06-852b-5b5358e447c7', 'zh-cn', '五花手链 (副本3)', '以梵克雅宝Lucky Spring系列为灵感蓝本，融合西班牙阿尔罕布拉宫建筑纹样与东方自然元素', '五朵立体雕刻花卉（如四叶草、梅花、铃兰）以黄金分割比例串联，寓意“五重幸运守护”，花瓣镶嵌红玉髓、珍珠母贝、孔雀石等天然宝石，通过0.03mm钻石刀头微雕工艺呈现细腻纹路。链节间采用“三点悬浮系统”，内置航天级润滑剂，可承受10万次开合磨损。', '标准链长18.5cm（无调节扣，适配14-18cm腕围），定制款可选15.5-21.5cm', '文化价值​：四叶草符号传承千年凯尔特文明，融合伊斯兰建筑美学，兼具博物馆级艺术性与日常佩戴场景', '先化妆喷香水，最后佩戴手链', '梵克雅宝同款天然宝石五花手链女18K金幸运四叶草轻奢手饰', '手工捶揲18K金五花手链，镶嵌南太平洋珍珠母贝+巴西红玉髓，以西班牙阿尔罕布拉宫黄金比例串联五重幸运符号。适配职场通勤/宴会晚装，磁吸搭扣经10万次开合测试，赠送定制防氧化礼盒', '五花手链、四叶草手链、招财手链、18K金手链', '2025-06-06 00:14:01.055741', '2025-06-06 00:14:01.055741');
INSERT INTO "public"."product_translations" VALUES ('704778c9-9f88-4d09-8b7d-12e5c4384545', '10893657-5b79-4a06-852b-5b5358e447c7', 'en-us', 'Five-Flower Bracelet (副本3)', 'Inspired by Van Cleef & Arpels'' Lucky Spring collection, blending the architectural motifs of Spain''s Alhambra Palace with Eastern natural elements', 'Five three-dimensionally carved flowers (such as four-leaf clovers, plum blossoms, and lilies of the valley) are connected in golden ratio proportions, symbolizing ''Fivefold Luck Protection.'' The petals are inlaid with natural gemstones like carnelian, mother-of-pearl, and malachite, showcasing intricate details through 0.03mm diamond-tip micro-carving. The links feature a ''Three-Point Suspension System'' with aerospace-grade lubricant, capable of withstanding 100,000 open-close cycles.', 'Standard chain length: 18.5cm (non-adjustable, fits 14-18cm wrist circumference). Custom lengths available: 15.5-21.5cm.', 'Cultural Value: The four-leaf clover motif carries millennia of Celtic heritage, fused with Islamic architectural aesthetics, offering museum-grade artistry suitable for daily wear.', 'Apply makeup and perfume first, then wear the bracelet.', 'Van Cleef & Arpels-Inspired Five-Flower Bracelet for Women with Natural Gemstones, 18K Gold Lucky Four-Leaf Clover Luxury Jewelry', 'Hand-hammered 18K gold five-flower bracelet featuring South Pacific mother-of-pearl and Brazilian carnelian inlays, connecting five lucky symbols in Alhambra Palace''s golden ratio. Perfect for office wear or evening events, with magnetic clasp tested for 100,000 cycles. Includes custom anti-tarnish gift box.', 'five-flower bracelet, four-leaf clover bracelet, wealth-attracting bracelet, 18K gold bracelet', '2025-06-06 00:14:01.055741', '2025-06-06 00:14:01.055741');
INSERT INTO "public"."product_translations" VALUES ('a89821c3-28d7-46f0-b6d2-a49ef078f18e', '10893657-5b79-4a06-852b-5b5358e447c7', 'ja-jp', '五華ブレスレット (副本3)', 'ヴァン クリーフ＆アーペルのラッキースプリングコレクションをインスピレーションとし、スペインのアルハンブラ宮殿の建築模様と東洋の自然要素を融合させたデザイン', '立体彫刻された5つの花（クローバー、梅の花、スズランなど）が黄金比で連なり、「五重の幸運の守り」を意味します。花びらにはカーネリアン、パール母貝、マラカイトなどの天然石が埋め込まれ、0.03mmのダイヤモンドビットによる微細な彫刻技術で繊細な模様を表現。チェーン連結部には「三点浮遊システム」を採用し、航空宇宙級潤滑剤を内蔵、10万回の開閉に耐える耐久性を実現。', '標準チェーン長18.5cm（調節金具なし、14-18cmの手首周りに適合）、オーダーメイド版は15.5-21.5cmから選択可能', '文化的価値：クローバーシンボルは千年のケルト文明を継承し、イスラム建築美学と融合、博物館級の芸術性と日常着用シーンを兼ね備えています', '化粧と香水を付けた後、最後にブレスレットを着用してください', 'ヴァン クリーフ＆アーペル風天然石五華ブレスレット 18Kゴールド ラッキークローバー レディース軽奢華アクセサリー', '手打ち18Kゴールド製五華ブレスレット。南太平洋産パール母貝+ブラジル産カーネリアンを埋め込み、スペイン・アルハンブラ宮殿の黄金比で五つの幸運シンボルを連結。ビジネス通勤/パーティー夜会に適応、マグネットクラスプは10万回開閉テスト済み。特製酸化防止ギフトボックス付属', '五華ブレスレット, クローバーブレスレット, 開運ブレスレット, 18Kゴールドブレスレット', '2025-06-06 00:14:01.055741', '2025-06-06 00:14:01.055741');
INSERT INTO "public"."product_translations" VALUES ('65c5489a-ccf6-402d-b95c-e565ea799562', '10893657-5b79-4a06-852b-5b5358e447c7', 'th-th', 'สร้อยข้อมือดอกไม้ 5 ดอก (副本3)', 'ได้รับแรงบันดาลใจจากคอลเลกชัน Lucky Spring ของ Van Cleef & Arpels ผสมผสานลวดลายสถาปัตยกรรมจาก Alhambra Palace ของสเปนกับองค์ประกอบธรรมชาติแบบตะวันออก', 'ดอกไม้ 5 ดอก (เช่นใบโคลเวอร์, ดอกพลัม, ลิลลี่แห่งหุบเขา) ที่แกะสลักสามมิติเรียงกันตามสัดส่วนทองคำ แสดงถึง "การปกป้องแห่งโชคลาภ 5 ประการ" กลีบดอกไม้ประดับด้วยหินธรรมชาติเช่นคาร์เนเลียน, มุก, และมรกต โดยใช้เทคนิคการแกะสลักละเอียดด้วยหัวเพชร 0.03mm ข้อต่อสร้อยใช้ "ระบบแขวน 3 จุด" ที่มีสารหล่อลื่นระดับการบินและอวกาศภายใน ทนทานต่อการเปิด-ปิดได้ถึง 100,000 ครั้ง', 'ความยาวมาตรฐาน 18.5 ซม. (ไม่มีตัวปรับความยาว เหมาะกับเส้นรอบวงข้อมือ 14-18 ซม.) แบบสั่งทำพิเศษสามารถเลือกความยาวได้ตั้งแต่ 15.5-21.5 ซม.', 'คุณค่าทางวัฒนธรรม: สัญลักษณ์ใบโคลเวอร์สืบทอดอารยธรรมเซลติกที่มีอายุพันปี ผสมผสานกับสุนทรียศาสตร์สถาปัตยกรรมอิสลาม มีทั้งคุณค่าทางศิลปะระดับพิพิธภัณฑ์และเหมาะกับการสวมใส่ในชีวิตประจำวัน', 'แต่งหน้าและฉีดน้ำหอมก่อน แล้วจึงสวมสร้อยข้อมือ', 'สร้อยข้อมือดอกไม้ 5 ดอกสำหรับผู้หญิง แบบเดียวกับ Van Cleef & Arpels ทำจากทอง 18K พร้อมหินธรรมชาติ ใบโคลเวอร์นำโชค เครื่องประดับแฟชั่นสุดหรู', 'สร้อยข้อมือดอกไม้ 5 ดอกทำจากทอง 18K ตอกมือ ประดับด้วยมุกจากแปซิฟิกใต้และคาร์เนเลียนจากบราซิล เรียงกันตามสัดส่วนทองคำของ Alhambra Palace แสดงถึงสัญลักษณ์โชคลาภ 5 ประการ เหมาะสำหรับการทำงานหรืองานเลี้ยง มีตัวล็อกแม่เหล็กที่ผ่านการทดสอบการเปิด-ปิด 100,000 ครั้ง พร้อมกล่องของขวัญป้องกันการออกซิไดซ์', 'สร้อยข้อมือดอกไม้ 5 ดอก, สร้อยข้อมือใบโคลเวอร์, สร้อยข้อมือนำโชค, สร้อยข้อมือทอง 18K', '2025-06-06 00:14:01.055741', '2025-06-06 00:14:01.055741');
INSERT INTO "public"."product_translations" VALUES ('b678e92b-3ade-4e8a-96a3-1957d7889008', 'dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'zh-cn', '五花手链 (副本4)', '以梵克雅宝Lucky Spring系列为灵感蓝本，融合西班牙阿尔罕布拉宫建筑纹样与东方自然元素', '五朵立体雕刻花卉（如四叶草、梅花、铃兰）以黄金分割比例串联，寓意“五重幸运守护”，花瓣镶嵌红玉髓、珍珠母贝、孔雀石等天然宝石，通过0.03mm钻石刀头微雕工艺呈现细腻纹路。链节间采用“三点悬浮系统”，内置航天级润滑剂，可承受10万次开合磨损。', '标准链长18.5cm（无调节扣，适配14-18cm腕围），定制款可选15.5-21.5cm', '文化价值​：四叶草符号传承千年凯尔特文明，融合伊斯兰建筑美学，兼具博物馆级艺术性与日常佩戴场景', '先化妆喷香水，最后佩戴手链', '梵克雅宝同款天然宝石五花手链女18K金幸运四叶草轻奢手饰', '手工捶揲18K金五花手链，镶嵌南太平洋珍珠母贝+巴西红玉髓，以西班牙阿尔罕布拉宫黄金比例串联五重幸运符号。适配职场通勤/宴会晚装，磁吸搭扣经10万次开合测试，赠送定制防氧化礼盒', '五花手链、四叶草手链、招财手链、18K金手链', '2025-06-06 00:14:01.111297', '2025-06-06 00:14:01.111297');
INSERT INTO "public"."product_translations" VALUES ('e5c9c0cc-18cc-48e1-b90b-6a5db6927ebd', 'dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'en-us', 'Five-Flower Bracelet (副本4)', 'Inspired by Van Cleef & Arpels'' Lucky Spring collection, blending the architectural motifs of Spain''s Alhambra Palace with Eastern natural elements', 'Five three-dimensionally carved flowers (such as four-leaf clovers, plum blossoms, and lilies of the valley) are connected in golden ratio proportions, symbolizing ''Fivefold Luck Protection.'' The petals are inlaid with natural gemstones like carnelian, mother-of-pearl, and malachite, showcasing intricate details through 0.03mm diamond-tip micro-carving. The links feature a ''Three-Point Suspension System'' with aerospace-grade lubricant, capable of withstanding 100,000 open-close cycles.', 'Standard chain length: 18.5cm (non-adjustable, fits 14-18cm wrist circumference). Custom lengths available: 15.5-21.5cm.', 'Cultural Value: The four-leaf clover motif carries millennia of Celtic heritage, fused with Islamic architectural aesthetics, offering museum-grade artistry suitable for daily wear.', 'Apply makeup and perfume first, then wear the bracelet.', 'Van Cleef & Arpels-Inspired Five-Flower Bracelet for Women with Natural Gemstones, 18K Gold Lucky Four-Leaf Clover Luxury Jewelry', 'Hand-hammered 18K gold five-flower bracelet featuring South Pacific mother-of-pearl and Brazilian carnelian inlays, connecting five lucky symbols in Alhambra Palace''s golden ratio. Perfect for office wear or evening events, with magnetic clasp tested for 100,000 cycles. Includes custom anti-tarnish gift box.', 'five-flower bracelet, four-leaf clover bracelet, wealth-attracting bracelet, 18K gold bracelet', '2025-06-06 00:14:01.111297', '2025-06-06 00:14:01.111297');
INSERT INTO "public"."product_translations" VALUES ('eb470fea-feb2-4e6f-944c-a1f66e8bd765', 'dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'ja-jp', '五華ブレスレット (副本4)', 'ヴァン クリーフ＆アーペルのラッキースプリングコレクションをインスピレーションとし、スペインのアルハンブラ宮殿の建築模様と東洋の自然要素を融合させたデザイン', '立体彫刻された5つの花（クローバー、梅の花、スズランなど）が黄金比で連なり、「五重の幸運の守り」を意味します。花びらにはカーネリアン、パール母貝、マラカイトなどの天然石が埋め込まれ、0.03mmのダイヤモンドビットによる微細な彫刻技術で繊細な模様を表現。チェーン連結部には「三点浮遊システム」を採用し、航空宇宙級潤滑剤を内蔵、10万回の開閉に耐える耐久性を実現。', '標準チェーン長18.5cm（調節金具なし、14-18cmの手首周りに適合）、オーダーメイド版は15.5-21.5cmから選択可能', '文化的価値：クローバーシンボルは千年のケルト文明を継承し、イスラム建築美学と融合、博物館級の芸術性と日常着用シーンを兼ね備えています', '化粧と香水を付けた後、最後にブレスレットを着用してください', 'ヴァン クリーフ＆アーペル風天然石五華ブレスレット 18Kゴールド ラッキークローバー レディース軽奢華アクセサリー', '手打ち18Kゴールド製五華ブレスレット。南太平洋産パール母貝+ブラジル産カーネリアンを埋め込み、スペイン・アルハンブラ宮殿の黄金比で五つの幸運シンボルを連結。ビジネス通勤/パーティー夜会に適応、マグネットクラスプは10万回開閉テスト済み。特製酸化防止ギフトボックス付属', '五華ブレスレット, クローバーブレスレット, 開運ブレスレット, 18Kゴールドブレスレット', '2025-06-06 00:14:01.111297', '2025-06-06 00:14:01.111297');
INSERT INTO "public"."product_translations" VALUES ('c41f0aa6-c3bf-4d51-a715-f8ca36b56e25', 'dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'th-th', 'สร้อยข้อมือดอกไม้ 5 ดอก (副本4)', 'ได้รับแรงบันดาลใจจากคอลเลกชัน Lucky Spring ของ Van Cleef & Arpels ผสมผสานลวดลายสถาปัตยกรรมจาก Alhambra Palace ของสเปนกับองค์ประกอบธรรมชาติแบบตะวันออก', 'ดอกไม้ 5 ดอก (เช่นใบโคลเวอร์, ดอกพลัม, ลิลลี่แห่งหุบเขา) ที่แกะสลักสามมิติเรียงกันตามสัดส่วนทองคำ แสดงถึง "การปกป้องแห่งโชคลาภ 5 ประการ" กลีบดอกไม้ประดับด้วยหินธรรมชาติเช่นคาร์เนเลียน, มุก, และมรกต โดยใช้เทคนิคการแกะสลักละเอียดด้วยหัวเพชร 0.03mm ข้อต่อสร้อยใช้ "ระบบแขวน 3 จุด" ที่มีสารหล่อลื่นระดับการบินและอวกาศภายใน ทนทานต่อการเปิด-ปิดได้ถึง 100,000 ครั้ง', 'ความยาวมาตรฐาน 18.5 ซม. (ไม่มีตัวปรับความยาว เหมาะกับเส้นรอบวงข้อมือ 14-18 ซม.) แบบสั่งทำพิเศษสามารถเลือกความยาวได้ตั้งแต่ 15.5-21.5 ซม.', 'คุณค่าทางวัฒนธรรม: สัญลักษณ์ใบโคลเวอร์สืบทอดอารยธรรมเซลติกที่มีอายุพันปี ผสมผสานกับสุนทรียศาสตร์สถาปัตยกรรมอิสลาม มีทั้งคุณค่าทางศิลปะระดับพิพิธภัณฑ์และเหมาะกับการสวมใส่ในชีวิตประจำวัน', 'แต่งหน้าและฉีดน้ำหอมก่อน แล้วจึงสวมสร้อยข้อมือ', 'สร้อยข้อมือดอกไม้ 5 ดอกสำหรับผู้หญิง แบบเดียวกับ Van Cleef & Arpels ทำจากทอง 18K พร้อมหินธรรมชาติ ใบโคลเวอร์นำโชค เครื่องประดับแฟชั่นสุดหรู', 'สร้อยข้อมือดอกไม้ 5 ดอกทำจากทอง 18K ตอกมือ ประดับด้วยมุกจากแปซิฟิกใต้และคาร์เนเลียนจากบราซิล เรียงกันตามสัดส่วนทองคำของ Alhambra Palace แสดงถึงสัญลักษณ์โชคลาภ 5 ประการ เหมาะสำหรับการทำงานหรืองานเลี้ยง มีตัวล็อกแม่เหล็กที่ผ่านการทดสอบการเปิด-ปิด 100,000 ครั้ง พร้อมกล่องของขวัญป้องกันการออกซิไดซ์', 'สร้อยข้อมือดอกไม้ 5 ดอก, สร้อยข้อมือใบโคลเวอร์, สร้อยข้อมือนำโชค, สร้อยข้อมือทอง 18K', '2025-06-06 00:14:01.111297', '2025-06-06 00:14:01.111297');

-- ----------------------------
-- Table structure for products
-- ----------------------------
DROP TABLE IF EXISTS "public"."products";
CREATE TABLE "public"."products" (
  "id" uuid NOT NULL,
  "sku_code" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "status" "public"."productstatus" NOT NULL,
  "weight" float8,
  "width" float8,
  "height" float8,
  "length" float8,
  "is_featured" bool,
  "is_new" bool,
  "is_bestseller" bool,
  "is_customizable" bool,
  "tax_class" varchar(50) COLLATE "pg_catalog"."default",
  "sort_order" int4,
  "seo_title" varchar(255) COLLATE "pg_catalog"."default",
  "seo_description" varchar(500) COLLATE "pg_catalog"."default",
  "seo_keywords" varchar(255) COLLATE "pg_catalog"."default",
  "meta_data" json,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL,
  "name" varchar(255) COLLATE "pg_catalog"."default",
  "description" text COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "public"."products"."sku_code" IS '商品编码，唯一';
COMMENT ON COLUMN "public"."products"."status" IS '商品状态：草稿、上架、下架、已删除';
COMMENT ON COLUMN "public"."products"."weight" IS '商品重量(克)';
COMMENT ON COLUMN "public"."products"."width" IS '商品宽度(厘米)';
COMMENT ON COLUMN "public"."products"."height" IS '商品高度(厘米)';
COMMENT ON COLUMN "public"."products"."length" IS '商品长度(厘米)';
COMMENT ON COLUMN "public"."products"."is_featured" IS '是否推荐商品';
COMMENT ON COLUMN "public"."products"."is_new" IS '是否新品';
COMMENT ON COLUMN "public"."products"."is_bestseller" IS '是否畅销品';
COMMENT ON COLUMN "public"."products"."is_customizable" IS '是否支持定制';
COMMENT ON COLUMN "public"."products"."tax_class" IS '税务类别';
COMMENT ON COLUMN "public"."products"."sort_order" IS '排序顺序';
COMMENT ON COLUMN "public"."products"."seo_title" IS 'SEO标题';
COMMENT ON COLUMN "public"."products"."seo_description" IS 'SEO描述';
COMMENT ON COLUMN "public"."products"."seo_keywords" IS 'SEO关键词';
COMMENT ON COLUMN "public"."products"."meta_data" IS '元数据，存储其他扩展信息';
COMMENT ON COLUMN "public"."products"."name" IS '商品名称';
COMMENT ON COLUMN "public"."products"."description" IS '商品描述';

-- ----------------------------
-- Records of products
-- ----------------------------
INSERT INTO "public"."products" VALUES ('2304e61a-ce9a-48a2-94bf-bdacda1ed1de', 'DZ-0001', 'DRAFT', 30, 23, 1, 23, 'f', 't', 'f', 'f', NULL, 0, '玉石吊坠', '玉石吊坠', '玉石吊坠', 'null', '2025-05-28 05:26:01.176444', '2025-05-28 05:26:01.176444', '玉石吊坠', '玉石吊坠');
INSERT INTO "public"."products" VALUES ('8412d590-9bf6-47c9-a5fc-302f1847513c', 'SL-0001', 'ACTIVE', 20, 22, 1, 22, 't', 't', 't', 'f', NULL, 0, '五花手链', '五花手链', '五花手链', 'null', '2025-05-28 05:20:57.877957', '2025-05-28 06:33:10.681757', '五花手链', '五花手链');
INSERT INTO "public"."products" VALUES ('bad5392d-9231-4c72-82b9-2b61a40e53d5', 'DZ-0002', 'DRAFT', 30, 40, 1, 40, 't', 't', 't', 'f', NULL, 0, '龙形项链', '龙形项链', '龙形项链', 'null', '2025-05-28 06:26:14.784728', '2025-05-28 06:26:14.784728', '龙形项链', '龙形项链');
INSERT INTO "public"."products" VALUES ('4ed2ac2e-70c9-4679-a445-4076bf406fcd', 'SL-0001_COPY_1', 'ACTIVE', 20, 22, 1, 22, 't', 't', 't', 'f', NULL, 0, '五花手链', '五花手链', '五花手链', 'null', '2025-06-06 00:14:00.912441', '2025-06-06 00:14:00.912441', '五花手链 (副本1)', '五花手链');
INSERT INTO "public"."products" VALUES ('bed054b6-14cc-43fc-98d2-00ad7d14170b', 'SL-0001_COPY_2', 'ACTIVE', 20, 22, 1, 22, 't', 't', 't', 'f', NULL, 0, '五花手链', '五花手链', '五花手链', 'null', '2025-06-06 00:14:00.988247', '2025-06-06 00:14:00.988247', '五花手链 (副本2)', '五花手链');
INSERT INTO "public"."products" VALUES ('10893657-5b79-4a06-852b-5b5358e447c7', 'SL-0001_COPY_3', 'ACTIVE', 20, 22, 1, 22, 't', 't', 't', 'f', NULL, 0, '五花手链', '五花手链', '五花手链', 'null', '2025-06-06 00:14:01.046628', '2025-06-06 00:14:01.046628', '五花手链 (副本3)', '五花手链');
INSERT INTO "public"."products" VALUES ('dffc8901-296d-4e26-88e4-a2c9ccc4ce51', 'SL-0001_COPY_4', 'ACTIVE', 20, 22, 1, 22, 't', 't', 't', 'f', NULL, 0, '五花手链', '五花手链', '五花手链', 'null', '2025-06-06 00:14:01.102786', '2025-06-06 00:14:01.102786', '五花手链 (副本4)', '五花手链');

-- ----------------------------
-- Table structure for promotions
-- ----------------------------
DROP TABLE IF EXISTS "public"."promotions";
CREATE TABLE "public"."promotions" (
  "id" uuid NOT NULL,
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default",
  "type" "public"."promotiontype" NOT NULL,
  "is_active" bool,
  "start_date" timestamp(6) NOT NULL,
  "end_date" timestamp(6),
  "active_days" int4[],
  "active_hours_start" int4,
  "active_hours_end" int4,
  "discount_type" "public"."discounttype" NOT NULL,
  "discount_value" float8 NOT NULL,
  "min_order_amount" float8,
  "max_discount_amount" float8,
  "usage_limit" int4,
  "usage_count" int4,
  "applicable_countries" varchar[] COLLATE "pg_catalog"."default",
  "excluded_countries" varchar[] COLLATE "pg_catalog"."default",
  "applicable_currencies" varchar[] COLLATE "pg_catalog"."default",
  "customer_eligibility" varchar(50) COLLATE "pg_catalog"."default",
  "eligible_customer_groups" uuid[],
  "min_customer_orders" int4,
  "applicable_products" uuid[],
  "excluded_products" uuid[],
  "applicable_categories" uuid[],
  "excluded_categories" uuid[],
  "combination_strategy" varchar(50) COLLATE "pg_catalog"."default",
  "priority" int4,
  "image_url" varchar(255) COLLATE "pg_catalog"."default",
  "banner_url" varchar(255) COLLATE "pg_catalog"."default",
  "highlight_color" varchar(7) COLLATE "pg_catalog"."default",
  "is_featured" bool,
  "conditions" json,
  "cultural_theme" varchar(100) COLLATE "pg_catalog"."default",
  "intention_type" varchar(100) COLLATE "pg_catalog"."default",
  "meta_data" json,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."promotions"."name" IS '促销名称';
COMMENT ON COLUMN "public"."promotions"."description" IS '促销描述';
COMMENT ON COLUMN "public"."promotions"."type" IS '促销类型';
COMMENT ON COLUMN "public"."promotions"."is_active" IS '是否激活';
COMMENT ON COLUMN "public"."promotions"."start_date" IS '开始日期';
COMMENT ON COLUMN "public"."promotions"."end_date" IS '结束日期';
COMMENT ON COLUMN "public"."promotions"."active_days" IS '生效的星期几：0-6，空表示所有天';
COMMENT ON COLUMN "public"."promotions"."active_hours_start" IS '生效开始小时：0-23';
COMMENT ON COLUMN "public"."promotions"."active_hours_end" IS '生效结束小时：0-23';
COMMENT ON COLUMN "public"."promotions"."discount_type" IS '折扣类型';
COMMENT ON COLUMN "public"."promotions"."discount_value" IS '折扣值（百分比或金额）';
COMMENT ON COLUMN "public"."promotions"."min_order_amount" IS '最低订单金额';
COMMENT ON COLUMN "public"."promotions"."max_discount_amount" IS '最大折扣金额';
COMMENT ON COLUMN "public"."promotions"."usage_limit" IS '使用次数限制';
COMMENT ON COLUMN "public"."promotions"."usage_count" IS '已使用次数';
COMMENT ON COLUMN "public"."promotions"."applicable_countries" IS '适用国家代码';
COMMENT ON COLUMN "public"."promotions"."excluded_countries" IS '排除国家代码';
COMMENT ON COLUMN "public"."promotions"."applicable_currencies" IS '适用货币代码';
COMMENT ON COLUMN "public"."promotions"."customer_eligibility" IS '客户资格：all, new, existing, specific';
COMMENT ON COLUMN "public"."promotions"."eligible_customer_groups" IS '符合条件的客户组';
COMMENT ON COLUMN "public"."promotions"."min_customer_orders" IS '最低历史订单数';
COMMENT ON COLUMN "public"."promotions"."applicable_products" IS '适用产品ID';
COMMENT ON COLUMN "public"."promotions"."excluded_products" IS '排除产品ID';
COMMENT ON COLUMN "public"."promotions"."applicable_categories" IS '适用分类ID';
COMMENT ON COLUMN "public"."promotions"."excluded_categories" IS '排除分类ID';
COMMENT ON COLUMN "public"."promotions"."combination_strategy" IS '组合策略：stack(叠加), exclusive(独占), priority(优先)';
COMMENT ON COLUMN "public"."promotions"."priority" IS '优先级，数字越大优先级越高';
COMMENT ON COLUMN "public"."promotions"."image_url" IS '图片URL';
COMMENT ON COLUMN "public"."promotions"."banner_url" IS '横幅URL';
COMMENT ON COLUMN "public"."promotions"."highlight_color" IS '高亮颜色代码';
COMMENT ON COLUMN "public"."promotions"."is_featured" IS '是否推荐显示';
COMMENT ON COLUMN "public"."promotions"."conditions" IS '促销触发条件，复杂JSON结构';
COMMENT ON COLUMN "public"."promotions"."cultural_theme" IS '文化主题';
COMMENT ON COLUMN "public"."promotions"."intention_type" IS '意图类型';
COMMENT ON COLUMN "public"."promotions"."meta_data" IS '元数据';

-- ----------------------------
-- Records of promotions
-- ----------------------------

-- ----------------------------
-- Table structure for return_item
-- ----------------------------
DROP TABLE IF EXISTS "public"."return_item";
CREATE TABLE "public"."return_item" (
  "return_id" uuid NOT NULL,
  "order_item_id" uuid NOT NULL,
  "quantity" int4 NOT NULL,
  "reason" varchar(50) COLLATE "pg_catalog"."default",
  "reason_detail" text COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."return_item"."quantity" IS '退货数量';
COMMENT ON COLUMN "public"."return_item"."reason" IS '退货原因';
COMMENT ON COLUMN "public"."return_item"."reason_detail" IS '退货原因详情';

-- ----------------------------
-- Records of return_item
-- ----------------------------

-- ----------------------------
-- Table structure for role_permissions
-- ----------------------------
DROP TABLE IF EXISTS "public"."role_permissions";
CREATE TABLE "public"."role_permissions" (
  "id" uuid NOT NULL,
  "role_id" uuid NOT NULL,
  "permission_id" uuid NOT NULL,
  "created_at" timestamp(6) NOT NULL
)
;

-- ----------------------------
-- Records of role_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for roles
-- ----------------------------
DROP TABLE IF EXISTS "public"."roles";
CREATE TABLE "public"."roles" (
  "id" uuid NOT NULL,
  "name" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "description" varchar(200) COLLATE "pg_catalog"."default",
  "is_default" bool,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;

-- ----------------------------
-- Records of roles
-- ----------------------------
INSERT INTO "public"."roles" VALUES ('2b2f75a8-9408-4d96-bc7d-f92c79645c10', '管理员', '系统管理员，拥有所有权限', 'f', '2025-05-23 10:10:38.26808', '2025-05-23 10:10:38.26808');
INSERT INTO "public"."roles" VALUES ('5c01d32b-1199-4233-a772-90ae493f54bc', '运营', '系统运营人员，负责内容和产品管理', 'f', '2025-05-23 10:10:38.26808', '2025-05-23 10:10:38.26808');
INSERT INTO "public"."roles" VALUES ('03f59f10-b9c3-4a9b-88d2-3085340f6290', '客服', '客服人员，负责处理订单和客户问题', 't', '2025-05-23 10:10:38.26808', '2025-05-23 10:10:38.26808');

-- ----------------------------
-- Table structure for segment_customer
-- ----------------------------
DROP TABLE IF EXISTS "public"."segment_customer";
CREATE TABLE "public"."segment_customer" (
  "segment_id" uuid NOT NULL,
  "customer_id" uuid NOT NULL,
  "created_at" timestamp(6) NOT NULL
)
;

-- ----------------------------
-- Records of segment_customer
-- ----------------------------

-- ----------------------------
-- Table structure for shipment_item
-- ----------------------------
DROP TABLE IF EXISTS "public"."shipment_item";
CREATE TABLE "public"."shipment_item" (
  "shipment_id" uuid NOT NULL,
  "order_item_id" uuid NOT NULL,
  "quantity" int4 NOT NULL,
  "created_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."shipment_item"."quantity" IS '发货数量';

-- ----------------------------
-- Records of shipment_item
-- ----------------------------

-- ----------------------------
-- Table structure for shipment_items
-- ----------------------------
DROP TABLE IF EXISTS "public"."shipment_items";
CREATE TABLE "public"."shipment_items" (
  "id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "shipment_id" uuid NOT NULL,
  "order_item_id" uuid NOT NULL,
  "product_id" uuid NOT NULL,
  "sku_id" uuid,
  "product_name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "sku_code" varchar(50) COLLATE "pg_catalog"."default",
  "quantity_shipped" int4 NOT NULL,
  "unit_price" numeric(10,2) NOT NULL,
  "attributes" jsonb,
  "image_url" varchar(255) COLLATE "pg_catalog"."default",
  "weight_per_unit" float8,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of shipment_items
-- ----------------------------

-- ----------------------------
-- Table structure for shipment_tracking
-- ----------------------------
DROP TABLE IF EXISTS "public"."shipment_tracking";
CREATE TABLE "public"."shipment_tracking" (
  "id" uuid NOT NULL DEFAULT uuid_generate_v4(),
  "shipment_id" uuid NOT NULL,
  "tracking_status" "public"."trackingstatus" NOT NULL,
  "location" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default" NOT NULL,
  "operator_name" varchar(100) COLLATE "pg_catalog"."default",
  "timestamp" timestamp(6) NOT NULL,
  "is_auto_generated" bool DEFAULT true,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of shipment_tracking
-- ----------------------------

-- ----------------------------
-- Table structure for shipping_addresses
-- ----------------------------
DROP TABLE IF EXISTS "public"."shipping_addresses";
CREATE TABLE "public"."shipping_addresses" (
  "id" uuid NOT NULL,
  "order_id" uuid NOT NULL,
  "recipient_name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "recipient_phone" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "recipient_email" varchar(255) COLLATE "pg_catalog"."default",
  "address_line1" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "address_line2" varchar(255) COLLATE "pg_catalog"."default",
  "city" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "state" varchar(100) COLLATE "pg_catalog"."default",
  "country" varchar(2) COLLATE "pg_catalog"."default" NOT NULL,
  "postcode" varchar(20) COLLATE "pg_catalog"."default" NOT NULL,
  "delivery_instructions" text COLLATE "pg_catalog"."default",
  "is_business_address" bool,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."shipping_addresses"."order_id" IS '订单ID，暂时不设外键约束';
COMMENT ON COLUMN "public"."shipping_addresses"."recipient_name" IS '收货人姓名';
COMMENT ON COLUMN "public"."shipping_addresses"."recipient_phone" IS '收货人电话';
COMMENT ON COLUMN "public"."shipping_addresses"."recipient_email" IS '收货人邮箱';
COMMENT ON COLUMN "public"."shipping_addresses"."address_line1" IS '地址行1';
COMMENT ON COLUMN "public"."shipping_addresses"."address_line2" IS '地址行2';
COMMENT ON COLUMN "public"."shipping_addresses"."city" IS '城市';
COMMENT ON COLUMN "public"."shipping_addresses"."state" IS '州/省';
COMMENT ON COLUMN "public"."shipping_addresses"."country" IS '国家代码(ISO)';
COMMENT ON COLUMN "public"."shipping_addresses"."postcode" IS '邮编';
COMMENT ON COLUMN "public"."shipping_addresses"."delivery_instructions" IS '配送说明';
COMMENT ON COLUMN "public"."shipping_addresses"."is_business_address" IS '是否商业地址';

-- ----------------------------
-- Records of shipping_addresses
-- ----------------------------

-- ----------------------------
-- Table structure for shipping_carriers
-- ----------------------------
DROP TABLE IF EXISTS "public"."shipping_carriers";
CREATE TABLE "public"."shipping_carriers" (
  "id" uuid NOT NULL,
  "code" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "name_en" varchar(100) COLLATE "pg_catalog"."default",
  "logo_url" varchar(255) COLLATE "pg_catalog"."default",
  "website" varchar(255) COLLATE "pg_catalog"."default",
  "tracking_url_template" varchar(500) COLLATE "pg_catalog"."default",
  "has_api" bool,
  "api_endpoint" varchar(255) COLLATE "pg_catalog"."default",
  "api_key" varchar(255) COLLATE "pg_catalog"."default",
  "api_config" json,
  "contact_phone" varchar(50) COLLATE "pg_catalog"."default",
  "is_active" bool,
  "sort_order" int4,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."shipping_carriers"."code" IS '快递公司代码';
COMMENT ON COLUMN "public"."shipping_carriers"."name" IS '快递公司名称';
COMMENT ON COLUMN "public"."shipping_carriers"."name_en" IS '英文名称';
COMMENT ON COLUMN "public"."shipping_carriers"."logo_url" IS 'Logo URL';
COMMENT ON COLUMN "public"."shipping_carriers"."website" IS '官方网站';
COMMENT ON COLUMN "public"."shipping_carriers"."tracking_url_template" IS '物流查询URL模板，{tracking_number}为占位符';
COMMENT ON COLUMN "public"."shipping_carriers"."has_api" IS '是否有API接口';
COMMENT ON COLUMN "public"."shipping_carriers"."api_endpoint" IS 'API端点';
COMMENT ON COLUMN "public"."shipping_carriers"."api_key" IS 'API密钥';
COMMENT ON COLUMN "public"."shipping_carriers"."api_config" IS 'API配置信息';
COMMENT ON COLUMN "public"."shipping_carriers"."contact_phone" IS '客服电话';
COMMENT ON COLUMN "public"."shipping_carriers"."is_active" IS '是否激活';
COMMENT ON COLUMN "public"."shipping_carriers"."sort_order" IS '排序顺序';

-- ----------------------------
-- Records of shipping_carriers
-- ----------------------------
INSERT INTO "public"."shipping_carriers" VALUES ('9ecf5835-d4dd-4d7c-bf13-90b5cc2743a2', 'SF', '顺丰速运', 'SF Express', '/static/images/carriers/sf.png', 'https://www.sf-express.com', 'https://www.sf-express.com/chn/sc/dynamic_function/waybill/#search/bill-number/{tracking_number}', 't', 'https://bsp-oisp.sf-express.com', NULL, NULL, '95338', 't', 1, '2025-06-06 00:18:24.449043', '2025-06-06 00:18:24.449043');
INSERT INTO "public"."shipping_carriers" VALUES ('595cd752-9873-41d8-babe-1ce83427afe9', 'YTO', '圆通速递', 'YTO Express', '/static/images/carriers/yto.png', 'https://www.yto.net.cn', 'https://www.yto.net.cn/index/query/gzquery.html?bill_code={tracking_number}', 't', 'https://open.yto.net.cn', NULL, NULL, '95554', 't', 2, '2025-06-06 00:18:24.451058', '2025-06-06 00:18:24.451058');
INSERT INTO "public"."shipping_carriers" VALUES ('52396c92-4d13-48e6-92dd-5816f6ea157c', 'ZTO', '中通快递', 'ZTO Express', '/static/images/carriers/zto.png', 'https://www.zto.com', 'https://www.zto.com/GuestService/Bill?txtBill={tracking_number}', 't', 'https://japi.zto.com', NULL, NULL, '95311', 't', 3, '2025-06-06 00:18:24.453056', '2025-06-06 00:18:24.453056');
INSERT INTO "public"."shipping_carriers" VALUES ('021a0af5-72c1-4e4d-a91c-5ecfe229e44a', 'STO', '申通快递', 'STO Express', '/static/images/carriers/sto.png', 'https://www.sto.cn', 'https://www.sto.cn/query?billcode={tracking_number}', 't', 'https://open.sto.cn', NULL, NULL, '95543', 't', 4, '2025-06-06 00:18:24.453056', '2025-06-06 00:18:24.453056');
INSERT INTO "public"."shipping_carriers" VALUES ('0f340ab6-f3db-4409-a680-fea59b8afc5f', 'YD', '韵达速递', 'Yunda Express', '/static/images/carriers/yunda.png', 'https://www.yunda.com', 'https://www.yunda.com/query/{tracking_number}', 't', 'https://open.yunda.com', NULL, NULL, '95546', 't', 5, '2025-06-06 00:18:24.454056', '2025-06-06 00:18:24.454056');
INSERT INTO "public"."shipping_carriers" VALUES ('6c77e875-43cc-4064-b82a-1abbcc0ef39f', 'EMS', '中国邮政EMS', 'China Post EMS', '/static/images/carriers/ems.png', 'https://www.ems.com.cn', 'https://www.ems.com.cn/queryList?mailNum={tracking_number}', 't', 'https://api.ems.com.cn', NULL, NULL, '11183', 't', 6, '2025-06-06 00:18:24.455056', '2025-06-06 00:18:24.455056');
INSERT INTO "public"."shipping_carriers" VALUES ('c3f965b4-2742-480b-bdf1-d1e26968f920', 'JD', '京东物流', 'JD Logistics', '/static/images/carriers/jd.png', 'https://www.jdl.cn', 'https://www.jdl.cn/#/trackIndex?waybillCode={tracking_number}', 't', 'https://api.jdl.cn', NULL, NULL, '950616', 't', 7, '2025-06-06 00:18:24.455056', '2025-06-06 00:18:24.455056');
INSERT INTO "public"."shipping_carriers" VALUES ('af71a556-42d8-4017-90ea-abd93a1d58ce', 'BEST', '百世快递', 'Best Express', '/static/images/carriers/best.png', 'https://www.best-inc.com', 'https://www.800best.com/clientService/orderQuery.do?mailNo={tracking_number}', 't', 'https://open.800best.com', NULL, NULL, '400-956-5656', 't', 8, '2025-06-06 00:18:24.456564', '2025-06-06 00:18:24.456564');

-- ----------------------------
-- Table structure for shipping_methods
-- ----------------------------
DROP TABLE IF EXISTS "public"."shipping_methods";
CREATE TABLE "public"."shipping_methods" (
  "id" uuid NOT NULL,
  "code" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default",
  "estimated_days_min" int4,
  "estimated_days_max" int4,
  "base_cost" float8,
  "cost_per_kg" float8,
  "free_shipping_threshold" float8,
  "max_weight" float8,
  "max_dimensions" json,
  "is_active" bool,
  "sort_order" int4,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."shipping_methods"."code" IS '配送方式代码';
COMMENT ON COLUMN "public"."shipping_methods"."name" IS '配送方式名称';
COMMENT ON COLUMN "public"."shipping_methods"."description" IS '配送方式描述';
COMMENT ON COLUMN "public"."shipping_methods"."estimated_days_min" IS '预计最少天数';
COMMENT ON COLUMN "public"."shipping_methods"."estimated_days_max" IS '预计最多天数';
COMMENT ON COLUMN "public"."shipping_methods"."base_cost" IS '基础费用';
COMMENT ON COLUMN "public"."shipping_methods"."cost_per_kg" IS '每公斤费用';
COMMENT ON COLUMN "public"."shipping_methods"."free_shipping_threshold" IS '免邮门槛';
COMMENT ON COLUMN "public"."shipping_methods"."max_weight" IS '最大重量限制(kg)';
COMMENT ON COLUMN "public"."shipping_methods"."max_dimensions" IS '最大尺寸限制{length, width, height}';
COMMENT ON COLUMN "public"."shipping_methods"."is_active" IS '是否激活';
COMMENT ON COLUMN "public"."shipping_methods"."sort_order" IS '排序顺序';

-- ----------------------------
-- Records of shipping_methods
-- ----------------------------
INSERT INTO "public"."shipping_methods" VALUES ('7245c2b9-d0dc-447a-9974-7ae8e8bce3dc', 'STANDARD', '标准快递', '普通快递配送，3-7个工作日送达', 3, 7, 8, 2, 99, 30, '{"length": 100, "width": 100, "height": 100}', 't', 1, '2025-06-06 00:18:24.459571', '2025-06-06 00:18:24.459571');
INSERT INTO "public"."shipping_methods" VALUES ('78f32826-de99-4b57-bfec-9eed9eb42547', 'EXPRESS', '特快专递', '加急快递配送，1-3个工作日送达', 1, 3, 15, 5, 199, 20, '{"length": 80, "width": 80, "height": 80}', 't', 2, '2025-06-06 00:18:24.461571', '2025-06-06 00:18:24.461571');
INSERT INTO "public"."shipping_methods" VALUES ('1a1f8008-455f-4d21-a72b-19f2c9a6a2c2', 'SAME_DAY', '当日达', '当日送达服务，限指定城市', 0, 1, 25, 8, 299, 10, '{"length": 60, "width": 60, "height": 60}', 't', 3, '2025-06-06 00:18:24.461571', '2025-06-06 00:18:24.461571');
INSERT INTO "public"."shipping_methods" VALUES ('ec8e79d3-b374-4c40-b5b3-f3261b1b173d', 'ECONOMY', '经济快递', '经济型配送，5-10个工作日送达', 5, 10, 5, 1, 59, 50, '{"length": 120, "width": 120, "height": 120}', 't', 4, '2025-06-06 00:18:24.462572', '2025-06-06 00:18:24.462572');
INSERT INTO "public"."shipping_methods" VALUES ('74f4b954-54e1-4081-bbc9-bbb82970dd8b', 'PICKUP', '门店自提', '到指定门店自提商品', 1, 3, 0, 0, 0, 100, '{"length": 200, "width": 200, "height": 200}', 't', 5, '2025-06-06 00:18:24.463572', '2025-06-06 00:18:24.463572');

-- ----------------------------
-- Table structure for shipping_order_shipments
-- ----------------------------
DROP TABLE IF EXISTS "public"."shipping_order_shipments";
CREATE TABLE "public"."shipping_order_shipments" (
  "id" uuid NOT NULL,
  "order_id" uuid NOT NULL,
  "carrier_id" uuid,
  "shipping_method_id" uuid,
  "tracking_number" varchar(100) COLLATE "pg_catalog"."default",
  "shipping_cost" float8,
  "insurance_cost" float8,
  "weight" float8,
  "length" float8,
  "width" float8,
  "height" float8,
  "shipped_at" timestamp(6),
  "estimated_delivery_date" timestamp(6),
  "delivered_at" timestamp(6),
  "notes" text COLLATE "pg_catalog"."default",
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."shipping_order_shipments"."order_id" IS '订单ID，暂时不设外键约束';
COMMENT ON COLUMN "public"."shipping_order_shipments"."tracking_number" IS '快递单号';
COMMENT ON COLUMN "public"."shipping_order_shipments"."shipping_cost" IS '运费';
COMMENT ON COLUMN "public"."shipping_order_shipments"."insurance_cost" IS '保险费';
COMMENT ON COLUMN "public"."shipping_order_shipments"."weight" IS '包裹重量(kg)';
COMMENT ON COLUMN "public"."shipping_order_shipments"."length" IS '包裹长度(cm)';
COMMENT ON COLUMN "public"."shipping_order_shipments"."width" IS '包裹宽度(cm)';
COMMENT ON COLUMN "public"."shipping_order_shipments"."height" IS '包裹高度(cm)';
COMMENT ON COLUMN "public"."shipping_order_shipments"."shipped_at" IS '发货时间';
COMMENT ON COLUMN "public"."shipping_order_shipments"."estimated_delivery_date" IS '预计送达时间';
COMMENT ON COLUMN "public"."shipping_order_shipments"."delivered_at" IS '实际送达时间';
COMMENT ON COLUMN "public"."shipping_order_shipments"."notes" IS '备注信息';

-- ----------------------------
-- Records of shipping_order_shipments
-- ----------------------------

-- ----------------------------
-- Table structure for shipping_tracking_events
-- ----------------------------
DROP TABLE IF EXISTS "public"."shipping_tracking_events";
CREATE TABLE "public"."shipping_tracking_events" (
  "id" uuid NOT NULL,
  "shipment_id" uuid NOT NULL,
  "event_type" "public"."trackingeventtype" NOT NULL,
  "event_time" timestamp(6) NOT NULL,
  "description" text COLLATE "pg_catalog"."default" NOT NULL,
  "location" varchar(255) COLLATE "pg_catalog"."default",
  "facility_name" varchar(255) COLLATE "pg_catalog"."default",
  "source" varchar(50) COLLATE "pg_catalog"."default",
  "external_event_id" varchar(100) COLLATE "pg_catalog"."default",
  "is_milestone" bool,
  "created_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."shipping_tracking_events"."event_type" IS '事件类型';
COMMENT ON COLUMN "public"."shipping_tracking_events"."event_time" IS '事件时间';
COMMENT ON COLUMN "public"."shipping_tracking_events"."description" IS '事件描述';
COMMENT ON COLUMN "public"."shipping_tracking_events"."location" IS '事件发生地点';
COMMENT ON COLUMN "public"."shipping_tracking_events"."facility_name" IS '中转站/网点名称';
COMMENT ON COLUMN "public"."shipping_tracking_events"."source" IS '数据来源：manual(手工录入), api(API获取)';
COMMENT ON COLUMN "public"."shipping_tracking_events"."external_event_id" IS '外部事件ID';
COMMENT ON COLUMN "public"."shipping_tracking_events"."is_milestone" IS '是否里程碑事件';

-- ----------------------------
-- Records of shipping_tracking_events
-- ----------------------------

-- ----------------------------
-- Table structure for shipping_trackings
-- ----------------------------
DROP TABLE IF EXISTS "public"."shipping_trackings";
CREATE TABLE "public"."shipping_trackings" (
  "id" uuid NOT NULL,
  "order_id" uuid NOT NULL,
  "shipment_id" uuid,
  "carrier_id" uuid,
  "tracking_number" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "estimated_delivery_date" timestamp(6),
  "actual_delivery_date" timestamp(6),
  "current_location" varchar(255) COLLATE "pg_catalog"."default",
  "origin_location" varchar(255) COLLATE "pg_catalog"."default",
  "destination_location" varchar(255) COLLATE "pg_catalog"."default",
  "tracking_events" json,
  "last_event" json,
  "recipient_name" varchar(100) COLLATE "pg_catalog"."default",
  "recipient_signature" varchar(255) COLLATE "pg_catalog"."default",
  "proof_of_delivery_url" varchar(255) COLLATE "pg_catalog"."default",
  "proof_of_delivery_date" timestamp(6),
  "exception_details" text COLLATE "pg_catalog"."default",
  "exception_date" timestamp(6),
  "resolution_details" text COLLATE "pg_catalog"."default",
  "package_weight" float8,
  "package_dimensions" json,
  "number_of_packages" int4,
  "shipping_service" varchar(100) COLLATE "pg_catalog"."default",
  "tracking_url" varchar(255) COLLATE "pg_catalog"."default",
  "callback_url" varchar(255) COLLATE "pg_catalog"."default",
  "notify_customer" bool,
  "notifications_sent" json,
  "meta_data" json,
  "carrier_specific_data" json,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;
COMMENT ON COLUMN "public"."shipping_trackings"."tracking_number" IS '物流追踪号';
COMMENT ON COLUMN "public"."shipping_trackings"."estimated_delivery_date" IS '预计送达日期';
COMMENT ON COLUMN "public"."shipping_trackings"."actual_delivery_date" IS '实际送达日期';
COMMENT ON COLUMN "public"."shipping_trackings"."current_location" IS '当前位置';
COMMENT ON COLUMN "public"."shipping_trackings"."origin_location" IS '起始位置';
COMMENT ON COLUMN "public"."shipping_trackings"."destination_location" IS '目的位置';
COMMENT ON COLUMN "public"."shipping_trackings"."tracking_events" IS '追踪事件历史';
COMMENT ON COLUMN "public"."shipping_trackings"."last_event" IS '最后事件';
COMMENT ON COLUMN "public"."shipping_trackings"."recipient_name" IS '收件人姓名';
COMMENT ON COLUMN "public"."shipping_trackings"."recipient_signature" IS '收件人签名URL';
COMMENT ON COLUMN "public"."shipping_trackings"."proof_of_delivery_url" IS '送达证明URL';
COMMENT ON COLUMN "public"."shipping_trackings"."proof_of_delivery_date" IS '送达证明日期';
COMMENT ON COLUMN "public"."shipping_trackings"."exception_details" IS '异常详情';
COMMENT ON COLUMN "public"."shipping_trackings"."exception_date" IS '异常日期';
COMMENT ON COLUMN "public"."shipping_trackings"."resolution_details" IS '解决措施';
COMMENT ON COLUMN "public"."shipping_trackings"."package_weight" IS '包裹重量(克)';
COMMENT ON COLUMN "public"."shipping_trackings"."package_dimensions" IS '包裹尺寸，如{length, width, height}格式';
COMMENT ON COLUMN "public"."shipping_trackings"."number_of_packages" IS '包裹数量';
COMMENT ON COLUMN "public"."shipping_trackings"."shipping_service" IS '配送服务';
COMMENT ON COLUMN "public"."shipping_trackings"."tracking_url" IS '追踪URL';
COMMENT ON COLUMN "public"."shipping_trackings"."callback_url" IS '回调URL';
COMMENT ON COLUMN "public"."shipping_trackings"."notify_customer" IS '是否通知客户';
COMMENT ON COLUMN "public"."shipping_trackings"."notifications_sent" IS '已发送通知记录';
COMMENT ON COLUMN "public"."shipping_trackings"."meta_data" IS '额外元数据';
COMMENT ON COLUMN "public"."shipping_trackings"."carrier_specific_data" IS '承运商特定数据';

-- ----------------------------
-- Records of shipping_trackings
-- ----------------------------

-- ----------------------------
-- Table structure for shipping_zone_method
-- ----------------------------
DROP TABLE IF EXISTS "public"."shipping_zone_method";
CREATE TABLE "public"."shipping_zone_method" (
  "zone_id" uuid NOT NULL,
  "method_id" uuid NOT NULL,
  "created_at" timestamp(6) NOT NULL
)
;

-- ----------------------------
-- Records of shipping_zone_method
-- ----------------------------

-- ----------------------------
-- Table structure for sku_attribute_value
-- ----------------------------
DROP TABLE IF EXISTS "public"."sku_attribute_value";
CREATE TABLE "public"."sku_attribute_value" (
  "sku_id" uuid NOT NULL,
  "attribute_value_id" uuid NOT NULL,
  "created_at" timestamp(6) NOT NULL
)
;

-- ----------------------------
-- Records of sku_attribute_value
-- ----------------------------
INSERT INTO "public"."sku_attribute_value" VALUES ('4fe91b37-7bf8-4973-8411-391175eeeb96', 'a14079b3-2acd-4168-b992-692304ae0cb4', '2025-05-30 05:59:52.607142');
INSERT INTO "public"."sku_attribute_value" VALUES ('4fe91b37-7bf8-4973-8411-391175eeeb96', '50083ed7-8e4e-49a7-9859-9548458d6b09', '2025-05-30 05:59:52.607142');
INSERT INTO "public"."sku_attribute_value" VALUES ('4fe91b37-7bf8-4973-8411-391175eeeb96', 'c51c747e-8bd9-4fe8-9d03-e6d9f9c5f36f', '2025-06-05 23:39:48.891767');
INSERT INTO "public"."sku_attribute_value" VALUES ('55d21ca1-488e-49f1-adb7-727a491de7f8', 'a14079b3-2acd-4168-b992-692304ae0cb4', '2025-06-06 00:14:00.923537');
INSERT INTO "public"."sku_attribute_value" VALUES ('55d21ca1-488e-49f1-adb7-727a491de7f8', '50083ed7-8e4e-49a7-9859-9548458d6b09', '2025-06-06 00:14:00.923537');
INSERT INTO "public"."sku_attribute_value" VALUES ('55d21ca1-488e-49f1-adb7-727a491de7f8', 'c51c747e-8bd9-4fe8-9d03-e6d9f9c5f36f', '2025-06-06 00:14:00.925005');
INSERT INTO "public"."sku_attribute_value" VALUES ('c4d4aab9-825c-45c4-a182-3b7160a453da', 'a14079b3-2acd-4168-b992-692304ae0cb4', '2025-06-06 00:14:00.997362');
INSERT INTO "public"."sku_attribute_value" VALUES ('c4d4aab9-825c-45c4-a182-3b7160a453da', '50083ed7-8e4e-49a7-9859-9548458d6b09', '2025-06-06 00:14:00.998361');
INSERT INTO "public"."sku_attribute_value" VALUES ('c4d4aab9-825c-45c4-a182-3b7160a453da', 'c51c747e-8bd9-4fe8-9d03-e6d9f9c5f36f', '2025-06-06 00:14:00.998361');
INSERT INTO "public"."sku_attribute_value" VALUES ('38ee75e2-ee3d-4447-808d-ea3048eaacb8', 'a14079b3-2acd-4168-b992-692304ae0cb4', '2025-06-06 00:14:01.05263');
INSERT INTO "public"."sku_attribute_value" VALUES ('38ee75e2-ee3d-4447-808d-ea3048eaacb8', '50083ed7-8e4e-49a7-9859-9548458d6b09', '2025-06-06 00:14:01.054732');
INSERT INTO "public"."sku_attribute_value" VALUES ('38ee75e2-ee3d-4447-808d-ea3048eaacb8', 'c51c747e-8bd9-4fe8-9d03-e6d9f9c5f36f', '2025-06-06 00:14:01.054732');
INSERT INTO "public"."sku_attribute_value" VALUES ('6275b947-32df-4f92-851c-fb4070dcdd60', 'a14079b3-2acd-4168-b992-692304ae0cb4', '2025-06-06 00:14:01.109298');
INSERT INTO "public"."sku_attribute_value" VALUES ('6275b947-32df-4f92-851c-fb4070dcdd60', '50083ed7-8e4e-49a7-9859-9548458d6b09', '2025-06-06 00:14:01.110297');
INSERT INTO "public"."sku_attribute_value" VALUES ('6275b947-32df-4f92-851c-fb4070dcdd60', 'c51c747e-8bd9-4fe8-9d03-e6d9f9c5f36f', '2025-06-06 00:14:01.110297');

-- ----------------------------
-- Table structure for system_settings
-- ----------------------------
DROP TABLE IF EXISTS "public"."system_settings";
CREATE TABLE "public"."system_settings" (
  "id" uuid NOT NULL,
  "setting_key" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "setting_value" text COLLATE "pg_catalog"."default",
  "setting_type" varchar(20) COLLATE "pg_catalog"."default",
  "setting_group" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "description" varchar(255) COLLATE "pg_catalog"."default",
  "is_sensitive" bool,
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL,
  "updated_by" uuid
)
;
COMMENT ON COLUMN "public"."system_settings"."setting_type" IS '设置值类型，如''string'', ''number'', ''boolean'', ''json''等';
COMMENT ON COLUMN "public"."system_settings"."setting_group" IS '设置分组，如''security'', ''display'', ''notification''等';
COMMENT ON COLUMN "public"."system_settings"."is_sensitive" IS '是否敏感信息，如密钥等';

-- ----------------------------
-- Records of system_settings
-- ----------------------------

-- ----------------------------
-- Table structure for user_roles
-- ----------------------------
DROP TABLE IF EXISTS "public"."user_roles";
CREATE TABLE "public"."user_roles" (
  "id" uuid NOT NULL,
  "user_id" uuid NOT NULL,
  "role_id" uuid NOT NULL,
  "created_at" timestamp(6) NOT NULL
)
;

-- ----------------------------
-- Records of user_roles
-- ----------------------------

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS "public"."users";
CREATE TABLE "public"."users" (
  "id" uuid NOT NULL,
  "username" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "email" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "hashed_password" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "full_name" varchar(100) COLLATE "pg_catalog"."default",
  "is_active" bool,
  "is_superuser" bool,
  "phone_number" varchar(20) COLLATE "pg_catalog"."default",
  "last_login" timestamp(6),
  "created_at" timestamp(6) NOT NULL,
  "updated_at" timestamp(6) NOT NULL
)
;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO "public"."users" VALUES ('4b743dd6-1847-437c-b784-783f44c1a400', 'admin', 'admin@mutelusys.com', '$2b$12$OZp/WYHOmt6TDpIYdWt0.uskmPQVP8DlotAAdTlae4zs2rIZFib6i', '系统管理员', 't', 't', NULL, '2025-06-07 03:50:33.770365', '2025-05-23 10:10:38.276859', '2025-06-07 03:50:33.771878');

-- ----------------------------
-- Function structure for armor
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."armor"(bytea, _text, _text);
CREATE FUNCTION "public"."armor"(bytea, _text, _text)
  RETURNS "pg_catalog"."text" AS '$libdir/pgcrypto', 'pg_armor'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for armor
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."armor"(bytea);
CREATE FUNCTION "public"."armor"(bytea)
  RETURNS "pg_catalog"."text" AS '$libdir/pgcrypto', 'pg_armor'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for crypt
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."crypt"(text, text);
CREATE FUNCTION "public"."crypt"(text, text)
  RETURNS "pg_catalog"."text" AS '$libdir/pgcrypto', 'pg_crypt'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for dearmor
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."dearmor"(text);
CREATE FUNCTION "public"."dearmor"(text)
  RETURNS "pg_catalog"."bytea" AS '$libdir/pgcrypto', 'pg_dearmor'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for decrypt
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."decrypt"(bytea, bytea, text);
CREATE FUNCTION "public"."decrypt"(bytea, bytea, text)
  RETURNS "pg_catalog"."bytea" AS '$libdir/pgcrypto', 'pg_decrypt'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for decrypt_iv
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."decrypt_iv"(bytea, bytea, bytea, text);
CREATE FUNCTION "public"."decrypt_iv"(bytea, bytea, bytea, text)
  RETURNS "pg_catalog"."bytea" AS '$libdir/pgcrypto', 'pg_decrypt_iv'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for digest
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."digest"(text, text);
CREATE FUNCTION "public"."digest"(text, text)
  RETURNS "pg_catalog"."bytea" AS '$libdir/pgcrypto', 'pg_digest'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for digest
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."digest"(bytea, text);
CREATE FUNCTION "public"."digest"(bytea, text)
  RETURNS "pg_catalog"."bytea" AS '$libdir/pgcrypto', 'pg_digest'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for encrypt
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."encrypt"(bytea, bytea, text);
CREATE FUNCTION "public"."encrypt"(bytea, bytea, text)
  RETURNS "pg_catalog"."bytea" AS '$libdir/pgcrypto', 'pg_encrypt'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for encrypt_iv
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."encrypt_iv"(bytea, bytea, bytea, text);
CREATE FUNCTION "public"."encrypt_iv"(bytea, bytea, bytea, text)
  RETURNS "pg_catalog"."bytea" AS '$libdir/pgcrypto', 'pg_encrypt_iv'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for gen_random_bytes
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."gen_random_bytes"(int4);
CREATE FUNCTION "public"."gen_random_bytes"(int4)
  RETURNS "pg_catalog"."bytea" AS '$libdir/pgcrypto', 'pg_random_bytes'
  LANGUAGE c VOLATILE STRICT
  COST 1;

-- ----------------------------
-- Function structure for gen_random_uuid
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."gen_random_uuid"();
CREATE FUNCTION "public"."gen_random_uuid"()
  RETURNS "pg_catalog"."uuid" AS '$libdir/pgcrypto', 'pg_random_uuid'
  LANGUAGE c VOLATILE
  COST 1;

-- ----------------------------
-- Function structure for gen_salt
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."gen_salt"(text);
CREATE FUNCTION "public"."gen_salt"(text)
  RETURNS "pg_catalog"."text" AS '$libdir/pgcrypto', 'pg_gen_salt'
  LANGUAGE c VOLATILE STRICT
  COST 1;

-- ----------------------------
-- Function structure for gen_salt
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."gen_salt"(text, int4);
CREATE FUNCTION "public"."gen_salt"(text, int4)
  RETURNS "pg_catalog"."text" AS '$libdir/pgcrypto', 'pg_gen_salt_rounds'
  LANGUAGE c VOLATILE STRICT
  COST 1;

-- ----------------------------
-- Function structure for hmac
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."hmac"(text, text, text);
CREATE FUNCTION "public"."hmac"(text, text, text)
  RETURNS "pg_catalog"."bytea" AS '$libdir/pgcrypto', 'pg_hmac'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for hmac
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."hmac"(bytea, bytea, text);
CREATE FUNCTION "public"."hmac"(bytea, bytea, text)
  RETURNS "pg_catalog"."bytea" AS '$libdir/pgcrypto', 'pg_hmac'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for pgp_armor_headers
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."pgp_armor_headers"(text, OUT "key" text, OUT "value" text);
CREATE FUNCTION "public"."pgp_armor_headers"(IN text, OUT "key" text, OUT "value" text)
  RETURNS SETOF "pg_catalog"."record" AS '$libdir/pgcrypto', 'pgp_armor_headers'
  LANGUAGE c IMMUTABLE STRICT
  COST 1
  ROWS 1000;

-- ----------------------------
-- Function structure for pgp_key_id
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."pgp_key_id"(bytea);
CREATE FUNCTION "public"."pgp_key_id"(bytea)
  RETURNS "pg_catalog"."text" AS '$libdir/pgcrypto', 'pgp_key_id_w'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for pgp_pub_decrypt
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."pgp_pub_decrypt"(bytea, bytea);
CREATE FUNCTION "public"."pgp_pub_decrypt"(bytea, bytea)
  RETURNS "pg_catalog"."text" AS '$libdir/pgcrypto', 'pgp_pub_decrypt_text'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for pgp_pub_decrypt
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."pgp_pub_decrypt"(bytea, bytea, text);
CREATE FUNCTION "public"."pgp_pub_decrypt"(bytea, bytea, text)
  RETURNS "pg_catalog"."text" AS '$libdir/pgcrypto', 'pgp_pub_decrypt_text'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for pgp_pub_decrypt
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."pgp_pub_decrypt"(bytea, bytea, text, text);
CREATE FUNCTION "public"."pgp_pub_decrypt"(bytea, bytea, text, text)
  RETURNS "pg_catalog"."text" AS '$libdir/pgcrypto', 'pgp_pub_decrypt_text'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for pgp_pub_decrypt_bytea
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."pgp_pub_decrypt_bytea"(bytea, bytea);
CREATE FUNCTION "public"."pgp_pub_decrypt_bytea"(bytea, bytea)
  RETURNS "pg_catalog"."bytea" AS '$libdir/pgcrypto', 'pgp_pub_decrypt_bytea'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for pgp_pub_decrypt_bytea
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."pgp_pub_decrypt_bytea"(bytea, bytea, text);
CREATE FUNCTION "public"."pgp_pub_decrypt_bytea"(bytea, bytea, text)
  RETURNS "pg_catalog"."bytea" AS '$libdir/pgcrypto', 'pgp_pub_decrypt_bytea'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for pgp_pub_decrypt_bytea
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."pgp_pub_decrypt_bytea"(bytea, bytea, text, text);
CREATE FUNCTION "public"."pgp_pub_decrypt_bytea"(bytea, bytea, text, text)
  RETURNS "pg_catalog"."bytea" AS '$libdir/pgcrypto', 'pgp_pub_decrypt_bytea'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for pgp_pub_encrypt
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."pgp_pub_encrypt"(text, bytea);
CREATE FUNCTION "public"."pgp_pub_encrypt"(text, bytea)
  RETURNS "pg_catalog"."bytea" AS '$libdir/pgcrypto', 'pgp_pub_encrypt_text'
  LANGUAGE c VOLATILE STRICT
  COST 1;

-- ----------------------------
-- Function structure for pgp_pub_encrypt
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."pgp_pub_encrypt"(text, bytea, text);
CREATE FUNCTION "public"."pgp_pub_encrypt"(text, bytea, text)
  RETURNS "pg_catalog"."bytea" AS '$libdir/pgcrypto', 'pgp_pub_encrypt_text'
  LANGUAGE c VOLATILE STRICT
  COST 1;

-- ----------------------------
-- Function structure for pgp_pub_encrypt_bytea
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."pgp_pub_encrypt_bytea"(bytea, bytea, text);
CREATE FUNCTION "public"."pgp_pub_encrypt_bytea"(bytea, bytea, text)
  RETURNS "pg_catalog"."bytea" AS '$libdir/pgcrypto', 'pgp_pub_encrypt_bytea'
  LANGUAGE c VOLATILE STRICT
  COST 1;

-- ----------------------------
-- Function structure for pgp_pub_encrypt_bytea
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."pgp_pub_encrypt_bytea"(bytea, bytea);
CREATE FUNCTION "public"."pgp_pub_encrypt_bytea"(bytea, bytea)
  RETURNS "pg_catalog"."bytea" AS '$libdir/pgcrypto', 'pgp_pub_encrypt_bytea'
  LANGUAGE c VOLATILE STRICT
  COST 1;

-- ----------------------------
-- Function structure for pgp_sym_decrypt
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."pgp_sym_decrypt"(bytea, text);
CREATE FUNCTION "public"."pgp_sym_decrypt"(bytea, text)
  RETURNS "pg_catalog"."text" AS '$libdir/pgcrypto', 'pgp_sym_decrypt_text'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for pgp_sym_decrypt
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."pgp_sym_decrypt"(bytea, text, text);
CREATE FUNCTION "public"."pgp_sym_decrypt"(bytea, text, text)
  RETURNS "pg_catalog"."text" AS '$libdir/pgcrypto', 'pgp_sym_decrypt_text'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for pgp_sym_decrypt_bytea
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."pgp_sym_decrypt_bytea"(bytea, text);
CREATE FUNCTION "public"."pgp_sym_decrypt_bytea"(bytea, text)
  RETURNS "pg_catalog"."bytea" AS '$libdir/pgcrypto', 'pgp_sym_decrypt_bytea'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for pgp_sym_decrypt_bytea
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."pgp_sym_decrypt_bytea"(bytea, text, text);
CREATE FUNCTION "public"."pgp_sym_decrypt_bytea"(bytea, text, text)
  RETURNS "pg_catalog"."bytea" AS '$libdir/pgcrypto', 'pgp_sym_decrypt_bytea'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for pgp_sym_encrypt
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."pgp_sym_encrypt"(text, text);
CREATE FUNCTION "public"."pgp_sym_encrypt"(text, text)
  RETURNS "pg_catalog"."bytea" AS '$libdir/pgcrypto', 'pgp_sym_encrypt_text'
  LANGUAGE c VOLATILE STRICT
  COST 1;

-- ----------------------------
-- Function structure for pgp_sym_encrypt
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."pgp_sym_encrypt"(text, text, text);
CREATE FUNCTION "public"."pgp_sym_encrypt"(text, text, text)
  RETURNS "pg_catalog"."bytea" AS '$libdir/pgcrypto', 'pgp_sym_encrypt_text'
  LANGUAGE c VOLATILE STRICT
  COST 1;

-- ----------------------------
-- Function structure for pgp_sym_encrypt_bytea
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."pgp_sym_encrypt_bytea"(bytea, text, text);
CREATE FUNCTION "public"."pgp_sym_encrypt_bytea"(bytea, text, text)
  RETURNS "pg_catalog"."bytea" AS '$libdir/pgcrypto', 'pgp_sym_encrypt_bytea'
  LANGUAGE c VOLATILE STRICT
  COST 1;

-- ----------------------------
-- Function structure for pgp_sym_encrypt_bytea
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."pgp_sym_encrypt_bytea"(bytea, text);
CREATE FUNCTION "public"."pgp_sym_encrypt_bytea"(bytea, text)
  RETURNS "pg_catalog"."bytea" AS '$libdir/pgcrypto', 'pgp_sym_encrypt_bytea'
  LANGUAGE c VOLATILE STRICT
  COST 1;

-- ----------------------------
-- Function structure for uuid_generate_v1
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."uuid_generate_v1"();
CREATE FUNCTION "public"."uuid_generate_v1"()
  RETURNS "pg_catalog"."uuid" AS '$libdir/uuid-ossp', 'uuid_generate_v1'
  LANGUAGE c VOLATILE STRICT
  COST 1;

-- ----------------------------
-- Function structure for uuid_generate_v1mc
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."uuid_generate_v1mc"();
CREATE FUNCTION "public"."uuid_generate_v1mc"()
  RETURNS "pg_catalog"."uuid" AS '$libdir/uuid-ossp', 'uuid_generate_v1mc'
  LANGUAGE c VOLATILE STRICT
  COST 1;

-- ----------------------------
-- Function structure for uuid_generate_v3
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."uuid_generate_v3"("namespace" uuid, "name" text);
CREATE FUNCTION "public"."uuid_generate_v3"("namespace" uuid, "name" text)
  RETURNS "pg_catalog"."uuid" AS '$libdir/uuid-ossp', 'uuid_generate_v3'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for uuid_generate_v4
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."uuid_generate_v4"();
CREATE FUNCTION "public"."uuid_generate_v4"()
  RETURNS "pg_catalog"."uuid" AS '$libdir/uuid-ossp', 'uuid_generate_v4'
  LANGUAGE c VOLATILE STRICT
  COST 1;

-- ----------------------------
-- Function structure for uuid_generate_v5
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."uuid_generate_v5"("namespace" uuid, "name" text);
CREATE FUNCTION "public"."uuid_generate_v5"("namespace" uuid, "name" text)
  RETURNS "pg_catalog"."uuid" AS '$libdir/uuid-ossp', 'uuid_generate_v5'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for uuid_nil
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."uuid_nil"();
CREATE FUNCTION "public"."uuid_nil"()
  RETURNS "pg_catalog"."uuid" AS '$libdir/uuid-ossp', 'uuid_nil'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for uuid_ns_dns
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."uuid_ns_dns"();
CREATE FUNCTION "public"."uuid_ns_dns"()
  RETURNS "pg_catalog"."uuid" AS '$libdir/uuid-ossp', 'uuid_ns_dns'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for uuid_ns_oid
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."uuid_ns_oid"();
CREATE FUNCTION "public"."uuid_ns_oid"()
  RETURNS "pg_catalog"."uuid" AS '$libdir/uuid-ossp', 'uuid_ns_oid'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for uuid_ns_url
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."uuid_ns_url"();
CREATE FUNCTION "public"."uuid_ns_url"()
  RETURNS "pg_catalog"."uuid" AS '$libdir/uuid-ossp', 'uuid_ns_url'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Function structure for uuid_ns_x500
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."uuid_ns_x500"();
CREATE FUNCTION "public"."uuid_ns_x500"()
  RETURNS "pg_catalog"."uuid" AS '$libdir/uuid-ossp', 'uuid_ns_x500'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;

-- ----------------------------
-- Primary Key structure for table blacklists
-- ----------------------------
ALTER TABLE "public"."blacklists" ADD CONSTRAINT "blacklists_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table bundle_intent
-- ----------------------------
ALTER TABLE "public"."bundle_intent" ADD CONSTRAINT "bundle_intent_pkey" PRIMARY KEY ("bundle_id", "intent_id");

-- ----------------------------
-- Primary Key structure for table bundle_items
-- ----------------------------
ALTER TABLE "public"."bundle_items" ADD CONSTRAINT "bundle_items_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table bundle_theme
-- ----------------------------
ALTER TABLE "public"."bundle_theme" ADD CONSTRAINT "bundle_theme_pkey" PRIMARY KEY ("bundle_id", "theme_id");

-- ----------------------------
-- Uniques structure for table carriers
-- ----------------------------
ALTER TABLE "public"."carriers" ADD CONSTRAINT "carriers_code_key" UNIQUE ("code");

-- ----------------------------
-- Primary Key structure for table carriers
-- ----------------------------
ALTER TABLE "public"."carriers" ADD CONSTRAINT "carriers_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table cash_on_delivery_settings
-- ----------------------------
ALTER TABLE "public"."cash_on_delivery_settings" ADD CONSTRAINT "cash_on_delivery_settings_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table coupon_batches
-- ----------------------------
ALTER TABLE "public"."coupon_batches" ADD CONSTRAINT "coupon_batches_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table coupons
-- ----------------------------
ALTER TABLE "public"."coupons" ADD CONSTRAINT "coupons_code_key" UNIQUE ("code");

-- ----------------------------
-- Primary Key structure for table coupons
-- ----------------------------
ALTER TABLE "public"."coupons" ADD CONSTRAINT "coupons_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table currencies
-- ----------------------------
ALTER TABLE "public"."currencies" ADD CONSTRAINT "currencies_code_key" UNIQUE ("code");

-- ----------------------------
-- Primary Key structure for table currencies
-- ----------------------------
ALTER TABLE "public"."currencies" ADD CONSTRAINT "currencies_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table currency_rates
-- ----------------------------
CREATE INDEX "idx_currency_rate_effective_date" ON "public"."currency_rates" USING btree (
  "effective_date" "pg_catalog"."timestamp_ops" ASC NULLS LAST
);
CREATE INDEX "idx_currency_rate_from_to" ON "public"."currency_rates" USING btree (
  "from_currency" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST,
  "to_currency" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Uniques structure for table currency_rates
-- ----------------------------
ALTER TABLE "public"."currency_rates" ADD CONSTRAINT "uix_currency_rate_active" UNIQUE ("from_currency", "to_currency", "effective_date", "is_active");

-- ----------------------------
-- Primary Key structure for table currency_rates
-- ----------------------------
ALTER TABLE "public"."currency_rates" ADD CONSTRAINT "currency_rates_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table customer_addresses
-- ----------------------------
ALTER TABLE "public"."customer_addresses" ADD CONSTRAINT "customer_addresses_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table customer_behaviors
-- ----------------------------
ALTER TABLE "public"."customer_behaviors" ADD CONSTRAINT "customer_behaviors_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table customer_coupons
-- ----------------------------
ALTER TABLE "public"."customer_coupons" ADD CONSTRAINT "customer_coupons_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table customer_cultural_preference
-- ----------------------------
ALTER TABLE "public"."customer_cultural_preference" ADD CONSTRAINT "customer_cultural_preference_pkey" PRIMARY KEY ("customer_id", "symbol_id");

-- ----------------------------
-- Primary Key structure for table customer_cultural_preference_details
-- ----------------------------
ALTER TABLE "public"."customer_cultural_preference_details" ADD CONSTRAINT "customer_cultural_preference_details_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table customer_group
-- ----------------------------
ALTER TABLE "public"."customer_group" ADD CONSTRAINT "customer_group_pkey" PRIMARY KEY ("customer_id", "group_id");

-- ----------------------------
-- Uniques structure for table customer_groups
-- ----------------------------
ALTER TABLE "public"."customer_groups" ADD CONSTRAINT "customer_groups_name_key" UNIQUE ("name");

-- ----------------------------
-- Primary Key structure for table customer_groups
-- ----------------------------
ALTER TABLE "public"."customer_groups" ADD CONSTRAINT "customer_groups_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table customer_intent
-- ----------------------------
ALTER TABLE "public"."customer_intent" ADD CONSTRAINT "customer_intent_pkey" PRIMARY KEY ("customer_id", "intent_id");

-- ----------------------------
-- Primary Key structure for table customer_intent_details
-- ----------------------------
ALTER TABLE "public"."customer_intent_details" ADD CONSTRAINT "customer_intent_details_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table customer_points
-- ----------------------------
ALTER TABLE "public"."customer_points" ADD CONSTRAINT "customer_points_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table customer_scene_preference
-- ----------------------------
ALTER TABLE "public"."customer_scene_preference" ADD CONSTRAINT "customer_scene_preference_pkey" PRIMARY KEY ("customer_id", "scene_id");

-- ----------------------------
-- Primary Key structure for table customer_scene_preference_details
-- ----------------------------
ALTER TABLE "public"."customer_scene_preference_details" ADD CONSTRAINT "customer_scene_preference_details_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table customer_segments
-- ----------------------------
ALTER TABLE "public"."customer_segments" ADD CONSTRAINT "customer_segments_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table customers
-- ----------------------------
CREATE UNIQUE INDEX "ix_customers_email" ON "public"."customers" USING btree (
  "email" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Uniques structure for table customers
-- ----------------------------
ALTER TABLE "public"."customers" ADD CONSTRAINT "customers_referral_code_key" UNIQUE ("referral_code");

-- ----------------------------
-- Primary Key structure for table customers
-- ----------------------------
ALTER TABLE "public"."customers" ADD CONSTRAINT "customers_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table data_backups
-- ----------------------------
ALTER TABLE "public"."data_backups" ADD CONSTRAINT "data_backups_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table email_verification_codes
-- ----------------------------
CREATE INDEX "idx_email_verification_codes_email" ON "public"."email_verification_codes" USING btree (
  "email" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_email_verification_codes_expires" ON "public"."email_verification_codes" USING btree (
  "expires_at" "pg_catalog"."timestamp_ops" ASC NULLS LAST
);
CREATE INDEX "idx_email_verification_codes_lookup" ON "public"."email_verification_codes" USING btree (
  "email" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST,
  "purpose" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST,
  "expires_at" "pg_catalog"."timestamp_ops" ASC NULLS LAST,
  "is_used" "pg_catalog"."bool_ops" ASC NULLS LAST
);
CREATE INDEX "ix_email_verification_codes_email" ON "public"."email_verification_codes" USING btree (
  "email" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table email_verification_codes
-- ----------------------------
ALTER TABLE "public"."email_verification_codes" ADD CONSTRAINT "email_verification_codes_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table gift_orders
-- ----------------------------
ALTER TABLE "public"."gift_orders" ADD CONSTRAINT "gift_orders_order_id_key" UNIQUE ("order_id");

-- ----------------------------
-- Primary Key structure for table gift_orders
-- ----------------------------
ALTER TABLE "public"."gift_orders" ADD CONSTRAINT "gift_orders_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table gift_registries
-- ----------------------------
ALTER TABLE "public"."gift_registries" ADD CONSTRAINT "gift_registries_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table gift_registry_items
-- ----------------------------
ALTER TABLE "public"."gift_registry_items" ADD CONSTRAINT "gift_registry_items_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table gift_registry_purchases
-- ----------------------------
ALTER TABLE "public"."gift_registry_purchases" ADD CONSTRAINT "gift_registry_purchases_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table gift_wrappings
-- ----------------------------
ALTER TABLE "public"."gift_wrappings" ADD CONSTRAINT "gift_wrappings_code_key" UNIQUE ("code");

-- ----------------------------
-- Primary Key structure for table gift_wrappings
-- ----------------------------
ALTER TABLE "public"."gift_wrappings" ADD CONSTRAINT "gift_wrappings_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table installment_plans
-- ----------------------------
ALTER TABLE "public"."installment_plans" ADD CONSTRAINT "installment_plans_code_key" UNIQUE ("code");

-- ----------------------------
-- Primary Key structure for table installment_plans
-- ----------------------------
ALTER TABLE "public"."installment_plans" ADD CONSTRAINT "installment_plans_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table inventory_history
-- ----------------------------
ALTER TABLE "public"."inventory_history" ADD CONSTRAINT "inventory_history_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table login_logs
-- ----------------------------
ALTER TABLE "public"."login_logs" ADD CONSTRAINT "login_logs_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table operation_logs
-- ----------------------------
ALTER TABLE "public"."operation_logs" ADD CONSTRAINT "operation_logs_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table order_items
-- ----------------------------
CREATE INDEX "idx_order_items_order_id" ON "public"."order_items" USING btree (
  "order_id" "pg_catalog"."uuid_ops" ASC NULLS LAST
);
CREATE INDEX "idx_order_items_product_id" ON "public"."order_items" USING btree (
  "product_id" "pg_catalog"."uuid_ops" ASC NULLS LAST
);
CREATE INDEX "idx_order_items_sku_id" ON "public"."order_items" USING btree (
  "sku_id" "pg_catalog"."uuid_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table order_items
-- ----------------------------
ALTER TABLE "public"."order_items" ADD CONSTRAINT "order_items_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table order_returns
-- ----------------------------
CREATE UNIQUE INDEX "ix_order_returns_return_number" ON "public"."order_returns" USING btree (
  "return_number" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table order_returns
-- ----------------------------
ALTER TABLE "public"."order_returns" ADD CONSTRAINT "order_returns_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table order_shipments
-- ----------------------------
CREATE INDEX "idx_order_shipments_carrier_name" ON "public"."order_shipments" USING btree (
  "carrier_name" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_order_shipments_order_id" ON "public"."order_shipments" USING btree (
  "order_id" "pg_catalog"."uuid_ops" ASC NULLS LAST
);
CREATE INDEX "idx_order_shipments_tracking_number" ON "public"."order_shipments" USING btree (
  "tracking_number" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Uniques structure for table order_shipments
-- ----------------------------
ALTER TABLE "public"."order_shipments" ADD CONSTRAINT "order_shipments_shipment_code_key" UNIQUE ("shipment_code");

-- ----------------------------
-- Checks structure for table order_shipments
-- ----------------------------
ALTER TABLE "public"."order_shipments" ADD CONSTRAINT "order_shipments_weight_check" CHECK (weight > 0::double precision);

-- ----------------------------
-- Primary Key structure for table order_shipments
-- ----------------------------
ALTER TABLE "public"."order_shipments" ADD CONSTRAINT "order_shipments_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table orders
-- ----------------------------
CREATE INDEX "idx_orders_created_at" ON "public"."orders" USING btree (
  "created_at" "pg_catalog"."timestamp_ops" ASC NULLS LAST
);
CREATE INDEX "idx_orders_customer_id" ON "public"."orders" USING btree (
  "customer_id" "pg_catalog"."uuid_ops" ASC NULLS LAST
);
CREATE INDEX "idx_orders_order_number" ON "public"."orders" USING btree (
  "order_number" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_orders_status" ON "public"."orders" USING btree (
  "status" "pg_catalog"."enum_ops" ASC NULLS LAST
);

-- ----------------------------
-- Uniques structure for table orders
-- ----------------------------
ALTER TABLE "public"."orders" ADD CONSTRAINT "orders_order_number_key" UNIQUE ("order_number");

-- ----------------------------
-- Primary Key structure for table orders
-- ----------------------------
ALTER TABLE "public"."orders" ADD CONSTRAINT "orders_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table payment_gateways
-- ----------------------------
ALTER TABLE "public"."payment_gateways" ADD CONSTRAINT "payment_gateways_code_key" UNIQUE ("code");

-- ----------------------------
-- Primary Key structure for table payment_gateways
-- ----------------------------
ALTER TABLE "public"."payment_gateways" ADD CONSTRAINT "payment_gateways_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table payment_logs
-- ----------------------------
ALTER TABLE "public"."payment_logs" ADD CONSTRAINT "payment_logs_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table payment_methods
-- ----------------------------
ALTER TABLE "public"."payment_methods" ADD CONSTRAINT "payment_methods_code_key" UNIQUE ("code");

-- ----------------------------
-- Primary Key structure for table payment_methods
-- ----------------------------
ALTER TABLE "public"."payment_methods" ADD CONSTRAINT "payment_methods_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table payment_statuses
-- ----------------------------
ALTER TABLE "public"."payment_statuses" ADD CONSTRAINT "payment_statuses_code_key" UNIQUE ("code");

-- ----------------------------
-- Primary Key structure for table payment_statuses
-- ----------------------------
ALTER TABLE "public"."payment_statuses" ADD CONSTRAINT "payment_statuses_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table payment_transactions
-- ----------------------------
ALTER TABLE "public"."payment_transactions" ADD CONSTRAINT "payment_transactions_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table permissions
-- ----------------------------
ALTER TABLE "public"."permissions" ADD CONSTRAINT "permissions_name_key" UNIQUE ("name");
ALTER TABLE "public"."permissions" ADD CONSTRAINT "permissions_code_key" UNIQUE ("code");

-- ----------------------------
-- Primary Key structure for table permissions
-- ----------------------------
ALTER TABLE "public"."permissions" ADD CONSTRAINT "permissions_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table product_attribute_values
-- ----------------------------
ALTER TABLE "public"."product_attribute_values" ADD CONSTRAINT "product_attribute_values_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table product_attributes
-- ----------------------------
CREATE UNIQUE INDEX "ix_product_attributes_code" ON "public"."product_attributes" USING btree (
  "code" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table product_attributes
-- ----------------------------
ALTER TABLE "public"."product_attributes" ADD CONSTRAINT "product_attributes_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table product_bundles
-- ----------------------------
CREATE UNIQUE INDEX "ix_product_bundles_sku_code" ON "public"."product_bundles" USING btree (
  "sku_code" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE UNIQUE INDEX "ix_product_bundles_slug" ON "public"."product_bundles" USING btree (
  "slug" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table product_bundles
-- ----------------------------
ALTER TABLE "public"."product_bundles" ADD CONSTRAINT "product_bundles_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table product_categories
-- ----------------------------
CREATE UNIQUE INDEX "ix_product_categories_slug" ON "public"."product_categories" USING btree (
  "slug" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table product_categories
-- ----------------------------
ALTER TABLE "public"."product_categories" ADD CONSTRAINT "product_categories_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table product_category
-- ----------------------------
ALTER TABLE "public"."product_category" ADD CONSTRAINT "product_category_pkey" PRIMARY KEY ("product_id", "category_id");

-- ----------------------------
-- Primary Key structure for table product_category_translations
-- ----------------------------
ALTER TABLE "public"."product_category_translations" ADD CONSTRAINT "product_category_translations_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table product_images
-- ----------------------------
CREATE INDEX "idx_product_images_is_video" ON "public"."product_images" USING btree (
  "is_video" "pg_catalog"."bool_ops" ASC NULLS LAST
);
CREATE INDEX "idx_product_images_video_format" ON "public"."product_images" USING btree (
  "video_format" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
) WHERE video_format IS NOT NULL;

-- ----------------------------
-- Primary Key structure for table product_images
-- ----------------------------
ALTER TABLE "public"."product_images" ADD CONSTRAINT "product_images_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table product_intent
-- ----------------------------
ALTER TABLE "public"."product_intent" ADD CONSTRAINT "product_intent_pkey" PRIMARY KEY ("product_id", "intent_id");

-- ----------------------------
-- Indexes structure for table product_intents
-- ----------------------------
CREATE UNIQUE INDEX "ix_product_intents_slug" ON "public"."product_intents" USING btree (
  "slug" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table product_intents
-- ----------------------------
ALTER TABLE "public"."product_intents" ADD CONSTRAINT "product_intents_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table product_inventories
-- ----------------------------
ALTER TABLE "public"."product_inventories" ADD CONSTRAINT "product_inventories_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table product_material
-- ----------------------------
ALTER TABLE "public"."product_material" ADD CONSTRAINT "product_material_pkey" PRIMARY KEY ("product_id", "material_id");

-- ----------------------------
-- Indexes structure for table product_materials
-- ----------------------------
CREATE UNIQUE INDEX "ix_product_materials_slug" ON "public"."product_materials" USING btree (
  "slug" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table product_materials
-- ----------------------------
ALTER TABLE "public"."product_materials" ADD CONSTRAINT "product_materials_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table product_prices
-- ----------------------------
ALTER TABLE "public"."product_prices" ADD CONSTRAINT "product_prices_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table product_scene
-- ----------------------------
ALTER TABLE "public"."product_scene" ADD CONSTRAINT "product_scene_pkey" PRIMARY KEY ("product_id", "scene_id");

-- ----------------------------
-- Indexes structure for table product_scenes
-- ----------------------------
CREATE UNIQUE INDEX "ix_product_scenes_slug" ON "public"."product_scenes" USING btree (
  "slug" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table product_scenes
-- ----------------------------
ALTER TABLE "public"."product_scenes" ADD CONSTRAINT "product_scenes_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table product_skus
-- ----------------------------
CREATE UNIQUE INDEX "ix_product_skus_sku_code" ON "public"."product_skus" USING btree (
  "sku_code" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table product_skus
-- ----------------------------
ALTER TABLE "public"."product_skus" ADD CONSTRAINT "product_skus_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table product_symbol
-- ----------------------------
ALTER TABLE "public"."product_symbol" ADD CONSTRAINT "product_symbol_pkey" PRIMARY KEY ("product_id", "symbol_id");

-- ----------------------------
-- Indexes structure for table product_symbols
-- ----------------------------
CREATE UNIQUE INDEX "ix_product_symbols_slug" ON "public"."product_symbols" USING btree (
  "slug" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table product_symbols
-- ----------------------------
ALTER TABLE "public"."product_symbols" ADD CONSTRAINT "product_symbols_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table product_tag
-- ----------------------------
ALTER TABLE "public"."product_tag" ADD CONSTRAINT "product_tag_pkey" PRIMARY KEY ("product_id", "tag_id");

-- ----------------------------
-- Indexes structure for table product_tags
-- ----------------------------
CREATE UNIQUE INDEX "ix_product_tags_slug" ON "public"."product_tags" USING btree (
  "slug" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table product_tags
-- ----------------------------
ALTER TABLE "public"."product_tags" ADD CONSTRAINT "product_tags_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table product_target_group
-- ----------------------------
ALTER TABLE "public"."product_target_group" ADD CONSTRAINT "product_target_group_pkey" PRIMARY KEY ("product_id", "target_group_id");

-- ----------------------------
-- Indexes structure for table product_target_groups
-- ----------------------------
CREATE UNIQUE INDEX "ix_product_target_groups_slug" ON "public"."product_target_groups" USING btree (
  "slug" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table product_target_groups
-- ----------------------------
ALTER TABLE "public"."product_target_groups" ADD CONSTRAINT "product_target_groups_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table product_theme
-- ----------------------------
ALTER TABLE "public"."product_theme" ADD CONSTRAINT "product_theme_pkey" PRIMARY KEY ("product_id", "theme_id");

-- ----------------------------
-- Indexes structure for table product_themes
-- ----------------------------
CREATE UNIQUE INDEX "ix_product_themes_slug" ON "public"."product_themes" USING btree (
  "slug" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table product_themes
-- ----------------------------
ALTER TABLE "public"."product_themes" ADD CONSTRAINT "product_themes_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table product_translations
-- ----------------------------
ALTER TABLE "public"."product_translations" ADD CONSTRAINT "product_translations_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table products
-- ----------------------------
CREATE UNIQUE INDEX "ix_products_sku_code" ON "public"."products" USING btree (
  "sku_code" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table products
-- ----------------------------
ALTER TABLE "public"."products" ADD CONSTRAINT "products_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table promotions
-- ----------------------------
ALTER TABLE "public"."promotions" ADD CONSTRAINT "promotions_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table return_item
-- ----------------------------
ALTER TABLE "public"."return_item" ADD CONSTRAINT "return_item_pkey" PRIMARY KEY ("return_id", "order_item_id");

-- ----------------------------
-- Primary Key structure for table role_permissions
-- ----------------------------
ALTER TABLE "public"."role_permissions" ADD CONSTRAINT "role_permissions_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table roles
-- ----------------------------
ALTER TABLE "public"."roles" ADD CONSTRAINT "roles_name_key" UNIQUE ("name");

-- ----------------------------
-- Primary Key structure for table roles
-- ----------------------------
ALTER TABLE "public"."roles" ADD CONSTRAINT "roles_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table segment_customer
-- ----------------------------
ALTER TABLE "public"."segment_customer" ADD CONSTRAINT "segment_customer_pkey" PRIMARY KEY ("segment_id", "customer_id");

-- ----------------------------
-- Primary Key structure for table shipment_item
-- ----------------------------
ALTER TABLE "public"."shipment_item" ADD CONSTRAINT "shipment_item_pkey" PRIMARY KEY ("shipment_id", "order_item_id");

-- ----------------------------
-- Primary Key structure for table shipment_items
-- ----------------------------
ALTER TABLE "public"."shipment_items" ADD CONSTRAINT "shipment_items_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table shipment_tracking
-- ----------------------------
CREATE INDEX "idx_shipment_tracking_location" ON "public"."shipment_tracking" USING btree (
  "location" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_shipment_tracking_timestamp" ON "public"."shipment_tracking" USING btree (
  "timestamp" "pg_catalog"."timestamp_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table shipment_tracking
-- ----------------------------
ALTER TABLE "public"."shipment_tracking" ADD CONSTRAINT "shipment_tracking_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table shipping_addresses
-- ----------------------------
ALTER TABLE "public"."shipping_addresses" ADD CONSTRAINT "shipping_addresses_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table shipping_carriers
-- ----------------------------
ALTER TABLE "public"."shipping_carriers" ADD CONSTRAINT "shipping_carriers_code_key" UNIQUE ("code");

-- ----------------------------
-- Primary Key structure for table shipping_carriers
-- ----------------------------
ALTER TABLE "public"."shipping_carriers" ADD CONSTRAINT "shipping_carriers_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table shipping_methods
-- ----------------------------
ALTER TABLE "public"."shipping_methods" ADD CONSTRAINT "shipping_methods_code_key" UNIQUE ("code");

-- ----------------------------
-- Primary Key structure for table shipping_methods
-- ----------------------------
ALTER TABLE "public"."shipping_methods" ADD CONSTRAINT "shipping_methods_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table shipping_order_shipments
-- ----------------------------
ALTER TABLE "public"."shipping_order_shipments" ADD CONSTRAINT "shipping_order_shipments_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table shipping_tracking_events
-- ----------------------------
ALTER TABLE "public"."shipping_tracking_events" ADD CONSTRAINT "shipping_tracking_events_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table shipping_trackings
-- ----------------------------
ALTER TABLE "public"."shipping_trackings" ADD CONSTRAINT "shipping_trackings_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table shipping_zone_method
-- ----------------------------
ALTER TABLE "public"."shipping_zone_method" ADD CONSTRAINT "shipping_zone_method_pkey" PRIMARY KEY ("zone_id", "method_id");

-- ----------------------------
-- Primary Key structure for table sku_attribute_value
-- ----------------------------
ALTER TABLE "public"."sku_attribute_value" ADD CONSTRAINT "sku_attribute_value_pkey" PRIMARY KEY ("sku_id", "attribute_value_id");

-- ----------------------------
-- Uniques structure for table system_settings
-- ----------------------------
ALTER TABLE "public"."system_settings" ADD CONSTRAINT "system_settings_setting_key_key" UNIQUE ("setting_key");

-- ----------------------------
-- Primary Key structure for table system_settings
-- ----------------------------
ALTER TABLE "public"."system_settings" ADD CONSTRAINT "system_settings_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table user_roles
-- ----------------------------
ALTER TABLE "public"."user_roles" ADD CONSTRAINT "user_roles_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table users
-- ----------------------------
CREATE UNIQUE INDEX "ix_users_email" ON "public"."users" USING btree (
  "email" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE UNIQUE INDEX "ix_users_username" ON "public"."users" USING btree (
  "username" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table users
-- ----------------------------
ALTER TABLE "public"."users" ADD CONSTRAINT "users_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Foreign Keys structure for table blacklists
-- ----------------------------
ALTER TABLE "public"."blacklists" ADD CONSTRAINT "blacklists_created_by_fkey" FOREIGN KEY ("created_by") REFERENCES "public"."users" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table bundle_intent
-- ----------------------------
ALTER TABLE "public"."bundle_intent" ADD CONSTRAINT "bundle_intent_bundle_id_fkey" FOREIGN KEY ("bundle_id") REFERENCES "public"."product_bundles" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."bundle_intent" ADD CONSTRAINT "bundle_intent_intent_id_fkey" FOREIGN KEY ("intent_id") REFERENCES "public"."product_intents" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table bundle_items
-- ----------------------------
ALTER TABLE "public"."bundle_items" ADD CONSTRAINT "bundle_items_bundle_id_fkey" FOREIGN KEY ("bundle_id") REFERENCES "public"."product_bundles" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."bundle_items" ADD CONSTRAINT "bundle_items_product_id_fkey" FOREIGN KEY ("product_id") REFERENCES "public"."products" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."bundle_items" ADD CONSTRAINT "bundle_items_sku_id_fkey" FOREIGN KEY ("sku_id") REFERENCES "public"."product_skus" ("id") ON DELETE SET NULL ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table bundle_theme
-- ----------------------------
ALTER TABLE "public"."bundle_theme" ADD CONSTRAINT "bundle_theme_bundle_id_fkey" FOREIGN KEY ("bundle_id") REFERENCES "public"."product_bundles" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."bundle_theme" ADD CONSTRAINT "bundle_theme_theme_id_fkey" FOREIGN KEY ("theme_id") REFERENCES "public"."product_themes" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table coupons
-- ----------------------------
ALTER TABLE "public"."coupons" ADD CONSTRAINT "coupons_batch_id_fkey" FOREIGN KEY ("batch_id") REFERENCES "public"."coupon_batches" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."coupons" ADD CONSTRAINT "coupons_free_product_id_fkey" FOREIGN KEY ("free_product_id") REFERENCES "public"."products" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."coupons" ADD CONSTRAINT "coupons_promotion_id_fkey" FOREIGN KEY ("promotion_id") REFERENCES "public"."promotions" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table customer_addresses
-- ----------------------------
ALTER TABLE "public"."customer_addresses" ADD CONSTRAINT "customer_addresses_customer_id_fkey" FOREIGN KEY ("customer_id") REFERENCES "public"."customers" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table customer_behaviors
-- ----------------------------
ALTER TABLE "public"."customer_behaviors" ADD CONSTRAINT "customer_behaviors_customer_id_fkey" FOREIGN KEY ("customer_id") REFERENCES "public"."customers" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table customer_coupons
-- ----------------------------
ALTER TABLE "public"."customer_coupons" ADD CONSTRAINT "customer_coupons_coupon_id_fkey" FOREIGN KEY ("coupon_id") REFERENCES "public"."coupons" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."customer_coupons" ADD CONSTRAINT "customer_coupons_customer_id_fkey" FOREIGN KEY ("customer_id") REFERENCES "public"."customers" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."customer_coupons" ADD CONSTRAINT "customer_coupons_issued_by_fkey" FOREIGN KEY ("issued_by") REFERENCES "public"."users" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."customer_coupons" ADD CONSTRAINT "customer_coupons_referrer_id_fkey" FOREIGN KEY ("referrer_id") REFERENCES "public"."customers" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table customer_cultural_preference
-- ----------------------------
ALTER TABLE "public"."customer_cultural_preference" ADD CONSTRAINT "customer_cultural_preference_customer_id_fkey" FOREIGN KEY ("customer_id") REFERENCES "public"."customers" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."customer_cultural_preference" ADD CONSTRAINT "customer_cultural_preference_symbol_id_fkey" FOREIGN KEY ("symbol_id") REFERENCES "public"."product_symbols" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table customer_cultural_preference_details
-- ----------------------------
ALTER TABLE "public"."customer_cultural_preference_details" ADD CONSTRAINT "customer_cultural_preference_details_customer_id_fkey" FOREIGN KEY ("customer_id") REFERENCES "public"."customers" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."customer_cultural_preference_details" ADD CONSTRAINT "customer_cultural_preference_details_symbol_id_fkey" FOREIGN KEY ("symbol_id") REFERENCES "public"."product_symbols" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table customer_group
-- ----------------------------
ALTER TABLE "public"."customer_group" ADD CONSTRAINT "customer_group_customer_id_fkey" FOREIGN KEY ("customer_id") REFERENCES "public"."customers" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."customer_group" ADD CONSTRAINT "customer_group_group_id_fkey" FOREIGN KEY ("group_id") REFERENCES "public"."customer_groups" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table customer_intent
-- ----------------------------
ALTER TABLE "public"."customer_intent" ADD CONSTRAINT "customer_intent_customer_id_fkey" FOREIGN KEY ("customer_id") REFERENCES "public"."customers" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."customer_intent" ADD CONSTRAINT "customer_intent_intent_id_fkey" FOREIGN KEY ("intent_id") REFERENCES "public"."product_intents" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table customer_intent_details
-- ----------------------------
ALTER TABLE "public"."customer_intent_details" ADD CONSTRAINT "customer_intent_details_customer_id_fkey" FOREIGN KEY ("customer_id") REFERENCES "public"."customers" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."customer_intent_details" ADD CONSTRAINT "customer_intent_details_intent_id_fkey" FOREIGN KEY ("intent_id") REFERENCES "public"."product_intents" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table customer_points
-- ----------------------------
ALTER TABLE "public"."customer_points" ADD CONSTRAINT "customer_points_customer_id_fkey" FOREIGN KEY ("customer_id") REFERENCES "public"."customers" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table customer_scene_preference
-- ----------------------------
ALTER TABLE "public"."customer_scene_preference" ADD CONSTRAINT "customer_scene_preference_customer_id_fkey" FOREIGN KEY ("customer_id") REFERENCES "public"."customers" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."customer_scene_preference" ADD CONSTRAINT "customer_scene_preference_scene_id_fkey" FOREIGN KEY ("scene_id") REFERENCES "public"."product_scenes" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table customer_scene_preference_details
-- ----------------------------
ALTER TABLE "public"."customer_scene_preference_details" ADD CONSTRAINT "customer_scene_preference_details_customer_id_fkey" FOREIGN KEY ("customer_id") REFERENCES "public"."customers" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."customer_scene_preference_details" ADD CONSTRAINT "customer_scene_preference_details_scene_id_fkey" FOREIGN KEY ("scene_id") REFERENCES "public"."product_scenes" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table customer_segments
-- ----------------------------
ALTER TABLE "public"."customer_segments" ADD CONSTRAINT "customer_segments_created_by_fkey" FOREIGN KEY ("created_by") REFERENCES "public"."users" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table customers
-- ----------------------------
ALTER TABLE "public"."customers" ADD CONSTRAINT "customers_referred_by_fkey" FOREIGN KEY ("referred_by") REFERENCES "public"."customers" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table data_backups
-- ----------------------------
ALTER TABLE "public"."data_backups" ADD CONSTRAINT "data_backups_created_by_fkey" FOREIGN KEY ("created_by") REFERENCES "public"."users" ("id") ON DELETE SET NULL ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table gift_orders
-- ----------------------------
ALTER TABLE "public"."gift_orders" ADD CONSTRAINT "gift_orders_registry_id_fkey" FOREIGN KEY ("registry_id") REFERENCES "public"."gift_registries" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table gift_registries
-- ----------------------------
ALTER TABLE "public"."gift_registries" ADD CONSTRAINT "gift_registries_customer_id_fkey" FOREIGN KEY ("customer_id") REFERENCES "public"."customers" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."gift_registries" ADD CONSTRAINT "gift_registries_shipping_address_id_fkey" FOREIGN KEY ("shipping_address_id") REFERENCES "public"."customer_addresses" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table gift_registry_items
-- ----------------------------
ALTER TABLE "public"."gift_registry_items" ADD CONSTRAINT "gift_registry_items_product_id_fkey" FOREIGN KEY ("product_id") REFERENCES "public"."products" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."gift_registry_items" ADD CONSTRAINT "gift_registry_items_registry_id_fkey" FOREIGN KEY ("registry_id") REFERENCES "public"."gift_registries" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."gift_registry_items" ADD CONSTRAINT "gift_registry_items_sku_id_fkey" FOREIGN KEY ("sku_id") REFERENCES "public"."product_skus" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table gift_registry_purchases
-- ----------------------------
ALTER TABLE "public"."gift_registry_purchases" ADD CONSTRAINT "gift_registry_purchases_registry_item_id_fkey" FOREIGN KEY ("registry_item_id") REFERENCES "public"."gift_registry_items" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table installment_plans
-- ----------------------------
ALTER TABLE "public"."installment_plans" ADD CONSTRAINT "installment_plans_payment_gateway_id_fkey" FOREIGN KEY ("payment_gateway_id") REFERENCES "public"."payment_gateways" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table inventory_history
-- ----------------------------
ALTER TABLE "public"."inventory_history" ADD CONSTRAINT "inventory_history_inventory_id_fkey" FOREIGN KEY ("inventory_id") REFERENCES "public"."product_inventories" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."inventory_history" ADD CONSTRAINT "inventory_history_operator_id_fkey" FOREIGN KEY ("operator_id") REFERENCES "public"."users" ("id") ON DELETE SET NULL ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table login_logs
-- ----------------------------
ALTER TABLE "public"."login_logs" ADD CONSTRAINT "login_logs_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table operation_logs
-- ----------------------------
ALTER TABLE "public"."operation_logs" ADD CONSTRAINT "operation_logs_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table order_items
-- ----------------------------
ALTER TABLE "public"."order_items" ADD CONSTRAINT "order_items_order_id_fkey" FOREIGN KEY ("order_id") REFERENCES "public"."orders" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table order_returns
-- ----------------------------
ALTER TABLE "public"."order_returns" ADD CONSTRAINT "order_returns_handler_id_fkey" FOREIGN KEY ("handler_id") REFERENCES "public"."users" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table payment_logs
-- ----------------------------
ALTER TABLE "public"."payment_logs" ADD CONSTRAINT "payment_logs_transaction_id_fkey" FOREIGN KEY ("transaction_id") REFERENCES "public"."payment_transactions" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."payment_logs" ADD CONSTRAINT "payment_logs_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table payment_methods
-- ----------------------------
ALTER TABLE "public"."payment_methods" ADD CONSTRAINT "payment_methods_gateway_id_fkey" FOREIGN KEY ("gateway_id") REFERENCES "public"."payment_gateways" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table payment_transactions
-- ----------------------------
ALTER TABLE "public"."payment_transactions" ADD CONSTRAINT "payment_transactions_customer_id_fkey" FOREIGN KEY ("customer_id") REFERENCES "public"."customers" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."payment_transactions" ADD CONSTRAINT "payment_transactions_parent_transaction_id_fkey" FOREIGN KEY ("parent_transaction_id") REFERENCES "public"."payment_transactions" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."payment_transactions" ADD CONSTRAINT "payment_transactions_payment_method_id_fkey" FOREIGN KEY ("payment_method_id") REFERENCES "public"."payment_methods" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table product_attribute_values
-- ----------------------------
ALTER TABLE "public"."product_attribute_values" ADD CONSTRAINT "product_attribute_values_attribute_id_fkey" FOREIGN KEY ("attribute_id") REFERENCES "public"."product_attributes" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table product_categories
-- ----------------------------
ALTER TABLE "public"."product_categories" ADD CONSTRAINT "product_categories_parent_id_fkey" FOREIGN KEY ("parent_id") REFERENCES "public"."product_categories" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table product_category
-- ----------------------------
ALTER TABLE "public"."product_category" ADD CONSTRAINT "product_category_category_id_fkey" FOREIGN KEY ("category_id") REFERENCES "public"."product_categories" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."product_category" ADD CONSTRAINT "product_category_product_id_fkey" FOREIGN KEY ("product_id") REFERENCES "public"."products" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table product_category_translations
-- ----------------------------
ALTER TABLE "public"."product_category_translations" ADD CONSTRAINT "product_category_translations_category_id_fkey" FOREIGN KEY ("category_id") REFERENCES "public"."product_categories" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table product_images
-- ----------------------------
ALTER TABLE "public"."product_images" ADD CONSTRAINT "product_images_product_id_fkey" FOREIGN KEY ("product_id") REFERENCES "public"."products" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table product_intent
-- ----------------------------
ALTER TABLE "public"."product_intent" ADD CONSTRAINT "product_intent_intent_id_fkey" FOREIGN KEY ("intent_id") REFERENCES "public"."product_intents" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."product_intent" ADD CONSTRAINT "product_intent_product_id_fkey" FOREIGN KEY ("product_id") REFERENCES "public"."products" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table product_inventories
-- ----------------------------
ALTER TABLE "public"."product_inventories" ADD CONSTRAINT "product_inventories_product_id_fkey" FOREIGN KEY ("product_id") REFERENCES "public"."products" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."product_inventories" ADD CONSTRAINT "product_inventories_sku_id_fkey" FOREIGN KEY ("sku_id") REFERENCES "public"."product_skus" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table product_material
-- ----------------------------
ALTER TABLE "public"."product_material" ADD CONSTRAINT "product_material_material_id_fkey" FOREIGN KEY ("material_id") REFERENCES "public"."product_materials" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."product_material" ADD CONSTRAINT "product_material_product_id_fkey" FOREIGN KEY ("product_id") REFERENCES "public"."products" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table product_materials
-- ----------------------------
ALTER TABLE "public"."product_materials" ADD CONSTRAINT "product_materials_parent_id_fkey" FOREIGN KEY ("parent_id") REFERENCES "public"."product_materials" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table product_prices
-- ----------------------------
ALTER TABLE "public"."product_prices" ADD CONSTRAINT "product_prices_product_id_fkey" FOREIGN KEY ("product_id") REFERENCES "public"."products" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table product_scene
-- ----------------------------
ALTER TABLE "public"."product_scene" ADD CONSTRAINT "product_scene_product_id_fkey" FOREIGN KEY ("product_id") REFERENCES "public"."products" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."product_scene" ADD CONSTRAINT "product_scene_scene_id_fkey" FOREIGN KEY ("scene_id") REFERENCES "public"."product_scenes" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table product_skus
-- ----------------------------
ALTER TABLE "public"."product_skus" ADD CONSTRAINT "product_skus_product_id_fkey" FOREIGN KEY ("product_id") REFERENCES "public"."products" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table product_symbol
-- ----------------------------
ALTER TABLE "public"."product_symbol" ADD CONSTRAINT "product_symbol_product_id_fkey" FOREIGN KEY ("product_id") REFERENCES "public"."products" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."product_symbol" ADD CONSTRAINT "product_symbol_symbol_id_fkey" FOREIGN KEY ("symbol_id") REFERENCES "public"."product_symbols" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table product_tag
-- ----------------------------
ALTER TABLE "public"."product_tag" ADD CONSTRAINT "product_tag_product_id_fkey" FOREIGN KEY ("product_id") REFERENCES "public"."products" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."product_tag" ADD CONSTRAINT "product_tag_tag_id_fkey" FOREIGN KEY ("tag_id") REFERENCES "public"."product_tags" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table product_target_group
-- ----------------------------
ALTER TABLE "public"."product_target_group" ADD CONSTRAINT "product_target_group_product_id_fkey" FOREIGN KEY ("product_id") REFERENCES "public"."products" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."product_target_group" ADD CONSTRAINT "product_target_group_target_group_id_fkey" FOREIGN KEY ("target_group_id") REFERENCES "public"."product_target_groups" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table product_theme
-- ----------------------------
ALTER TABLE "public"."product_theme" ADD CONSTRAINT "product_theme_product_id_fkey" FOREIGN KEY ("product_id") REFERENCES "public"."products" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."product_theme" ADD CONSTRAINT "product_theme_theme_id_fkey" FOREIGN KEY ("theme_id") REFERENCES "public"."product_themes" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table product_translations
-- ----------------------------
ALTER TABLE "public"."product_translations" ADD CONSTRAINT "product_translations_product_id_fkey" FOREIGN KEY ("product_id") REFERENCES "public"."products" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table return_item
-- ----------------------------
ALTER TABLE "public"."return_item" ADD CONSTRAINT "return_item_return_id_fkey" FOREIGN KEY ("return_id") REFERENCES "public"."order_returns" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table role_permissions
-- ----------------------------
ALTER TABLE "public"."role_permissions" ADD CONSTRAINT "role_permissions_permission_id_fkey" FOREIGN KEY ("permission_id") REFERENCES "public"."permissions" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."role_permissions" ADD CONSTRAINT "role_permissions_role_id_fkey" FOREIGN KEY ("role_id") REFERENCES "public"."roles" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table segment_customer
-- ----------------------------
ALTER TABLE "public"."segment_customer" ADD CONSTRAINT "segment_customer_customer_id_fkey" FOREIGN KEY ("customer_id") REFERENCES "public"."customers" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."segment_customer" ADD CONSTRAINT "segment_customer_segment_id_fkey" FOREIGN KEY ("segment_id") REFERENCES "public"."customer_segments" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table shipment_items
-- ----------------------------
ALTER TABLE "public"."shipment_items" ADD CONSTRAINT "fk_shipment_items_shipment" FOREIGN KEY ("shipment_id") REFERENCES "public"."order_shipments" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table shipment_tracking
-- ----------------------------
ALTER TABLE "public"."shipment_tracking" ADD CONSTRAINT "fk_shipment_tracking_shipment" FOREIGN KEY ("shipment_id") REFERENCES "public"."order_shipments" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table shipping_order_shipments
-- ----------------------------
ALTER TABLE "public"."shipping_order_shipments" ADD CONSTRAINT "shipping_order_shipments_carrier_id_fkey" FOREIGN KEY ("carrier_id") REFERENCES "public"."shipping_carriers" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."shipping_order_shipments" ADD CONSTRAINT "shipping_order_shipments_shipping_method_id_fkey" FOREIGN KEY ("shipping_method_id") REFERENCES "public"."shipping_methods" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table shipping_tracking_events
-- ----------------------------
ALTER TABLE "public"."shipping_tracking_events" ADD CONSTRAINT "shipping_tracking_events_shipment_id_fkey" FOREIGN KEY ("shipment_id") REFERENCES "public"."shipping_order_shipments" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table sku_attribute_value
-- ----------------------------
ALTER TABLE "public"."sku_attribute_value" ADD CONSTRAINT "sku_attribute_value_attribute_value_id_fkey" FOREIGN KEY ("attribute_value_id") REFERENCES "public"."product_attribute_values" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."sku_attribute_value" ADD CONSTRAINT "sku_attribute_value_sku_id_fkey" FOREIGN KEY ("sku_id") REFERENCES "public"."product_skus" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table system_settings
-- ----------------------------
ALTER TABLE "public"."system_settings" ADD CONSTRAINT "system_settings_updated_by_fkey" FOREIGN KEY ("updated_by") REFERENCES "public"."users" ("id") ON DELETE SET NULL ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table user_roles
-- ----------------------------
ALTER TABLE "public"."user_roles" ADD CONSTRAINT "user_roles_role_id_fkey" FOREIGN KEY ("role_id") REFERENCES "public"."roles" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."user_roles" ADD CONSTRAINT "user_roles_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."users" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
