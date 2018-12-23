CREATE TABLE `members` (
  `phoneNo` varchar(16) NOT NULL,
  `curriculumNo` int(10) NOT NULL,
  `attendanceCheck` text,
  `curriculumComplete` text,
  `employment` text,
  `insertedTimestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updatedTimestamp` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`phoneNo`,`curriculumNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
