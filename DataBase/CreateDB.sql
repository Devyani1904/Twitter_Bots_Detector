/*Twitter Bots MySQL Scripts*/
CREATE SCHEMA MyTwitter_bots;
use MyTwitter_bots;
CREATE TABLE `Matrix` (
  `idUser` bigint(20),
  `idFollowing` bigint(20),
  `Score` int(11) DEFAULT 0,
  `Ratio_FF` bigint(20) DEFAULT 0,
  `Description_Ind` int(11) DEFAULT 0,
  `Friend_Cnt_Ind` int(11) DEFAULT 0,
  `Default_Prof_Ind` int(11) DEFAULT 0,
  `Default_IMG_IND` int(11) DEFAULT 0,
  `Tweet_Per_Yr_Ind` int(11) DEFAULT 0,
  `Like_Per_Yr_Ind` int(11) DEFAULT 0,
  `Screen_name_IND` int(11) DEFAULT 0,
  `isVerified` int(11) DEFAULT NULL,
  PRIMARY KEY (`idUser`, `idFollowing`)
); 

CREATE TABLE `Tweets` (
  `seq_id` int(11) NOT NULL AUTO_INCREMENT,
  `screen_name` varchar(160) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `tweet_id` bigint(20) NOT NULL,
  `tweet_text` varchar(160) NOT NULL,
  `retweet_count` int(11) DEFAULT NULL,
  `favorite_count` int(11) DEFAULT NULL,
  `geo_enabled` tinyint(1) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`seq_id`)
);

CREATE TABLE `User` (
  `idUser` bigint(20) NOT NULL,
  `Name` varchar(50) DEFAULT NULL,
  `Description` varchar(200) DEFAULT NULL,
  `Followers_Count` int(11) DEFAULT NULL,
  `Friends_Count` int(11) DEFAULT NULL,
  `Statuses_Count` int(11) DEFAULT NULL,
  `Favourites_Count` int(11) DEFAULT NULL,
  `Screen_Name` varchar(50) DEFAULT NULL,
  `Created_At` datetime DEFAULT NULL,
  `Url` varchar(100) DEFAULT NULL,
  `Verified` tinyint(4) DEFAULT NULL,
  `Lang` varchar(45) DEFAULT NULL,
  `Default_Profile` tinyint(4) DEFAULT NULL,
  `Default_Profile_Image` tinyint(4) DEFAULT NULL,
  `Profile_Image_Url` varchar(100) DEFAULT NULL,
  `Profile_Background_Color` varchar(45) DEFAULT NULL,
  `Profile_Background_Image_Url` varchar(100) DEFAULT NULL,
  `Protected` bool DEFAULT False,
  PRIMARY KEY (`idUser`)
);

CREATE TABLE `UserFollower` (
	`idUser` bigint(20) NOT NULL,
    `idFollower` bigint(20) NOT NULL,
     PRIMARY KEY (`idUser`, `idFollower`)
);



USE `MyTwitter_bots`;
DROP procedure IF EXISTS `insertMatrixInformation_noTweetTable`;

DELIMITER $$
USE `MyTwitter_bots`$$
CREATE PROCEDURE  `insertMatrixInformation_noTweetTable`(IN in_screenName varchar(50))
BEGIN
	DECLARE yearToSecondsRatio bigint DEFAULT 31540000000;
	INSERT INTO MyTwitter_bots.Matrix(idUser, idFollowing, Ratio_FF,Description_Ind,Friend_Cnt_Ind,Default_prof_Ind,Default_IMG_IND,Tweet_Per_Yr_Ind,Like_Per_Yr_Ind,Screen_name_IND, isVerified)
	SELECT MyTwitter_bots.follower.idUser, mytwitter_bots.usr.idUser as idFollowing,
    CASE WHEN (follower.Friends_Count/follower.Followers_Count) > 10 THEN 3
				WHEN (follower.Friends_Count/follower.Followers_Count) > 8 THEN 2
				WHEN (follower.Friends_Count/follower.Followers_Count) > 5 THEN 1
				ELSE 0
			END AS Ratio_FF,
	CASE WHEN follower.DescriptioN = '' THEN 1 ELSE 0 END AS Description_Ind,
	CASE WHEN follower.Friends_Count >=1000 AND follower.Friends_Count <2000  THEN 1 
		 WHEN follower.Friends_Count >=2000 AND follower.Friends_Count <3000 THEN 2 
		 WHEN follower.Friends_Count >=3000 THEN 3
	ELSE 0 END AS Friend_Cnt_Ind,
	follower.Default_profile AS Default_prof_Ind,
	follower.Default_profile_image AS Default_IMG_IND,
	CASE WHEN follower.Statuses_Count / (timestampdiff(DAY, follower.created_at, now()) / 365) > 7000 THEN 3
				WHEN follower.Statuses_Count / (timestampdiff(DAY, follower.created_at, now()) / 365) > 5000 THEN 2
				WHEN follower.Statuses_Count / (timestampdiff(DAY, follower.created_at, now()) / 365) > 3000 THEN 1
				ELSE 0 END AS Tweet_Per_Yr_Ind,
	CASE WHEN follower.Favourites_Count / (timestampdiff(DAY, follower.created_at, now()) / 365) > 7000 THEN 3
				WHEN follower.Favourites_Count / (timestampdiff(DAY, follower.created_at, now()) / 365) > 5000 THEN 2
				WHEN follower.Favourites_Count / (timestampdiff(DAY, follower.created_at, now()) / 365) > 3000 THEN 1
				ELSE 0 END AS Like_Per_Yr_Ind,
	CASE when (length(regexp_replace(follower.Screen_Name, '[^0-9]', ''))/2) <= 4 Then 0
		 when (length(regexp_replace(follower.Screen_Name, '[^0-9]', ''))/2) > 4 Then 1		 
		 when (length(regexp_replace(follower.Screen_Name, '[^0-9]', ''))/2) > 6 Then 2
	END Screen_name_IND,
    CASE WHEN follower.Verified = 0 THEN 0 ELSE -99 END AS isVerified
	FROM MyTwitter_bots.User usr, mytwitter_bots.userfollower usrFollower, mytwitter_bots.user follower
	WHERE usr.Screen_name = in_screenName
    AND usr.idUser = usrFollower.idUser
    AND follower.idUser = usrFollower.idFollower;
	Commit; 
    
    SET SQL_SAFE_UPDATES = 0;
    UPDATE Matrix a, Matrix b SET a.Score = (b.Ratio_FF + b.Description_Ind + b.Friend_Cnt_Ind + b. Default_Prof_Ind + b.Default_IMG_IND + b.Tweet_Per_Yr_Ind + b.Like_Per_Yr_Ind + b.Screen_Name_IND + b.isVerified) WHERE a.idUser = b.idUser;
    SET SQL_SAFE_UPDATES = 1;
    Commit;
END$$

DELIMITER ;
