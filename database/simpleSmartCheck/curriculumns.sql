CREATE TABLE `curriculums` (
  `curriculumNo` int(10) NOT NULL AUTO_INCREMENT,
  `curriculumCategory` text NOT NULL,
  `ordinalNo` text NOT NULL,
  `curriculumName` text NOT NULL,
  `curriculumType` text NOT NULL,
  `startDate` date NOT NULL,
  `endDate` date NOT NULL,
  `applicantsInserted` text,
  `membersInserted` text,
  `insertedTimestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updatedTimestamp` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`curriculumNo`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;