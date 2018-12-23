CREATE TABLE `attendanceLogs` (
  `phoneNo` varchar(16) NOT NULL,
  `curriculumNo` int(10) NOT NULL,
  `checkInOut` text NOT NULL,
  `signature` text NOT NULL,
  `insertedTimestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updatedTimestamp` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`phoneNo`,`curriculumNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;