/*
 Navicat Premium Data Transfer

 Source Server         : tan
 Source Server Type    : MySQL
 Source Server Version : 80033
 Source Host           : localhost:3306
 Source Schema         : chatroom

 Target Server Type    : MySQL
 Target Server Version : 80033
 File Encoding         : 65001

 Date: 28/04/2023 15:32:04
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for chat_messages
-- ----------------------------
DROP TABLE IF EXISTS `chat_messages`;
CREATE TABLE `chat_messages`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `login_id` int NULL DEFAULT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `login_id`(`login_id` ASC) USING BTREE,
  CONSTRAINT `chat_messages_ibfk_1` FOREIGN KEY (`login_id`) REFERENCES `login` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 20 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of chat_messages
-- ----------------------------
INSERT INTO `chat_messages` VALUES (1, 3, '你们觉得ChatGPT如何？', '2023-04-25 14:02:35');
INSERT INTO `chat_messages` VALUES (2, 4, '我觉得ChatGPT很有用，因为它可以帮助我们回答一些问题，而且它的回答还可以让人觉得很自然', '2023-04-25 14:03:01');
INSERT INTO `chat_messages` VALUES (3, 5, '我也同意凯特的看法，但是我认为ChatGPT的回答并不总是准确的。有时候它会误解我们的问题，导致回答不够准确。', '2023-04-25 14:03:34');
INSERT INTO `chat_messages` VALUES (4, 6, '我认为ChatGPT在一些情况下很有用，但是在一些领域它的回答可能会有所偏颇，因为它并不是专业人士，不能提供专业的建议。', '2023-04-25 14:03:50');
INSERT INTO `chat_messages` VALUES (5, 3, '我同意你们的看法。ChatGPT的回答很大程度上取决于输入的问题。如果我们能够提供准确的问题，那么ChatGPT的回答也会更加准确。', '2023-04-25 14:04:05');
INSERT INTO `chat_messages` VALUES (6, 4, '另外，我认为我们需要时刻谨记，ChatGPT只是一个计算机程序，不能完全取代人类的智慧和判断力。', '2023-04-25 14:04:25');
INSERT INTO `chat_messages` VALUES (7, 5, '确实如此，我认为我们需要对ChatGPT的回答进行一些验证，以确保其准确性。', '2023-04-25 14:04:43');
INSERT INTO `chat_messages` VALUES (8, 6, '总的来说，我认为ChatGPT是一种非常有用的工具，但是我们需要明确它的局限性。', '2023-04-25 14:05:23');
INSERT INTO `chat_messages` VALUES (9, 3, '你们听说了吗，GPT5已经开发完成了。', '2023-04-25 14:07:05');
INSERT INTO `chat_messages` VALUES (10, 4, '我知道他学习了很多视频，我觉得AI的发展速度非常快，特别是在最近几年。', '2023-04-25 14:07:59');
INSERT INTO `chat_messages` VALUES (11, 5, '我也觉得AI发展太迅速了，他可能会取代很多的职业，我们该怎么办？', '2023-04-25 14:08:19');
INSERT INTO `chat_messages` VALUES (12, 6, '我觉得应该暂停AI的发展，我害怕我因为AI失业。', '2023-04-25 14:11:07');
INSERT INTO `chat_messages` VALUES (13, 4, '你不必担心AI取代你的工作，你应该利用他们提供你的效率，而不是抵制它。', '2023-04-25 14:12:11');
INSERT INTO `chat_messages` VALUES (14, 4, '我的下线了，再见', '2023-04-25 14:12:59');
INSERT INTO `chat_messages` VALUES (15, 5, '再见，改天在聊', '2023-04-25 14:13:26');
INSERT INTO `chat_messages` VALUES (16, 6, '886', '2023-04-25 14:13:43');
INSERT INTO `chat_messages` VALUES (17, 3, '我也得下了', '2023-04-25 14:14:06');
INSERT INTO `chat_messages` VALUES (18, 2, '管理员', '2023-04-25 17:14:39');
INSERT INTO `chat_messages` VALUES (19, 1, '1', '2023-04-25 17:14:47');

-- ----------------------------
-- Table structure for login
-- ----------------------------
DROP TABLE IF EXISTS `login`;
CREATE TABLE `login`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `role` enum('user','admin') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE,
  UNIQUE INDEX `email`(`email` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of login
-- ----------------------------
INSERT INTO `login` VALUES (1, 'admin', 'admin', 'null', 'admin');
INSERT INTO `login` VALUES (2, 'tan', 'tcw2829952', '1401685750@qq.com', 'user');
INSERT INTO `login` VALUES (3, '王伟', '12345678', '1@qq.com', 'user');
INSERT INTO `login` VALUES (4, '张莉', '12345678', '2@qq.com', 'user');
INSERT INTO `login` VALUES (5, '李明', '12345678', '3@qq.com', 'user');
INSERT INTO `login` VALUES (6, '赵丽', '12345678', '4@qq.com', 'user');

-- ----------------------------
-- Table structure for sentiment_analysis
-- ----------------------------
DROP TABLE IF EXISTS `sentiment_analysis`;
CREATE TABLE `sentiment_analysis`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `sentiment` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `positive_prob` float NULL DEFAULT NULL,
  `neutral_prob` float NULL DEFAULT NULL,
  `negative_prob` float NULL DEFAULT NULL,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `chat_message_id` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `chat_message_id`(`chat_message_id` ASC) USING BTREE,
  CONSTRAINT `sentiment_analysis_ibfk_1` FOREIGN KEY (`chat_message_id`) REFERENCES `chat_messages` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `sentiment_analysis_ibfk_2` FOREIGN KEY (`chat_message_id`) REFERENCES `chat_messages` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 20 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sentiment_analysis
-- ----------------------------
INSERT INTO `sentiment_analysis` VALUES (1, '正面语句', 0.9554, 0.036, 0.0085, '王伟', 1);
INSERT INTO `sentiment_analysis` VALUES (2, '正面语句', 0.9973, 0.0001, 0.0026, '张莉', 2);
INSERT INTO `sentiment_analysis` VALUES (3, '正面语句', 0.9572, 0.002, 0.0407, '李明', 3);
INSERT INTO `sentiment_analysis` VALUES (4, '正面语句', 0.9694, 0.0034, 0.0272, '赵丽', 4);
INSERT INTO `sentiment_analysis` VALUES (5, '正面语句', 0.9986, 0.0001, 0.0013, '王伟', 5);
INSERT INTO `sentiment_analysis` VALUES (6, '正面语句', 0.9915, 0, 0.0084, '张莉', 6);
INSERT INTO `sentiment_analysis` VALUES (7, '正面语句', 0.8982, 0.01, 0.0918, '李明', 7);
INSERT INTO `sentiment_analysis` VALUES (8, '正面语句', 0.9943, 0.0004, 0.0053, '赵丽', 8);
INSERT INTO `sentiment_analysis` VALUES (9, '正面语句', 0.9442, 0.0172, 0.0386, '王伟', 9);
INSERT INTO `sentiment_analysis` VALUES (10, '正面语句', 0.9916, 0.0001, 0.0083, '张莉', 10);
INSERT INTO `sentiment_analysis` VALUES (11, '正面语句', 0.9876, 0.0013, 0.011, '李明', 11);
INSERT INTO `sentiment_analysis` VALUES (12, '正面语句', 0.9894, 0.0004, 0.0103, '赵丽', 12);
INSERT INTO `sentiment_analysis` VALUES (13, '正面语句', 0.9492, 0.0278, 0.0229, '张莉', 13);
INSERT INTO `sentiment_analysis` VALUES (14, '负面语句', 0.0278, 0.0019, 0.9703, '张莉', 14);
INSERT INTO `sentiment_analysis` VALUES (15, '负面语句', 0.0454, 0.006, 0.9486, '李明', 15);
INSERT INTO `sentiment_analysis` VALUES (16, '正面语句', 0.9986, 0.0001, 0.0013, '赵丽', 16);
INSERT INTO `sentiment_analysis` VALUES (17, '负面语句', 0.1293, 0.0004, 0.8703, '王伟', 17);
INSERT INTO `sentiment_analysis` VALUES (18, '正面语句', 0.8453, 0.0679, 0.0866, 'tan', 18);
INSERT INTO `sentiment_analysis` VALUES (19, '正面语句', 0.6339, 0.1665, 0.1992, 'admin', 19);

-- ----------------------------
-- Table structure for user_profiles
-- ----------------------------
DROP TABLE IF EXISTS `user_profiles`;
CREATE TABLE `user_profiles`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `gender` enum('male','female','other') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `introduction` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `username`(`username` ASC) USING BTREE,
  CONSTRAINT `user_profiles_ibfk_1` FOREIGN KEY (`username`) REFERENCES `login` (`username`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_profiles
-- ----------------------------
INSERT INTO `user_profiles` VALUES (1, 'admin', 'other', NULL, NULL);
INSERT INTO `user_profiles` VALUES (2, 'tan', 'male', NULL, NULL);
INSERT INTO `user_profiles` VALUES (3, '王伟', 'male', NULL, NULL);
INSERT INTO `user_profiles` VALUES (4, '张莉', 'female', NULL, NULL);
INSERT INTO `user_profiles` VALUES (5, '李明', 'male', NULL, NULL);
INSERT INTO `user_profiles` VALUES (6, '赵丽', 'female', NULL, NULL);

-- ----------------------------
-- View structure for sentiment_analysis_view
-- ----------------------------
DROP VIEW IF EXISTS `sentiment_analysis_view`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `sentiment_analysis_view` AS select `sa`.`id` AS `id`,`sa`.`sentiment` AS `sentiment`,`sa`.`positive_prob` AS `positive_prob`,`sa`.`neutral_prob` AS `neutral_prob`,`sa`.`negative_prob` AS `negative_prob`,`l`.`username` AS `username` from ((`sentiment_analysis` `sa` join `chat_messages` `cm` on((`sa`.`chat_message_id` = `cm`.`id`))) join `login` `l` on((`cm`.`login_id` = `l`.`id`)));

-- ----------------------------
-- Triggers structure for table login
-- ----------------------------
DROP TRIGGER IF EXISTS `insert_user_profile`;
delimiter ;;
CREATE TRIGGER `insert_user_profile` AFTER INSERT ON `login` FOR EACH ROW BEGIN
  INSERT INTO user_profiles (username) VALUES (NEW.username);
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
