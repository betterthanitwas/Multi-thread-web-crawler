# create logical group of DB objects in DB (pg 241)
CREATE SCHEMA WEBCRAWL;

# tell mysql which db to use
USE WEBCRAWL;

CREATE TABLE SITE (
SITE_ID		BIGINT UNSIGNED		NOT NULL	UNIQUE	AUTO_INCREMENT,
SITE_URL	VARCHAR(255)		UNIQUE,	# make sure the URL is unique
SITE_TITLE	VARCHAR(100),
PRIMARY KEY (SITE_ID))
ENGINE = INNODB; # produces transaction - safe tables (pg. 247)

CREATE TABLE WORD (
WORD_ID		BIGINT UNSIGNED		NOT NULL	UNIQUE	AUTO_INCREMENT,
WORD_WORD	VARCHAR(45),
PRIMARY KEY (WORD_ID))
ENGINE = INNODB;

CREATE TABLE EXCERPT (
SITE_ID					BIGINT UNSIGNED,
WORD_ID					BIGINT UNSIGNED, # try adding index here to see if its faster on return...
EXCERPT_WRD_AMT_SITE	INT,
EXCERPT_PHRASE			VARCHAR(150),
PRIMARY KEY (SITE_ID, WORD_ID),
FOREIGN KEY	(SITE_ID) REFERENCES SITE(SITE_ID) ON DELETE CASCADE,
FOREIGN KEY (WORD_ID) REFERENCES WORD(WORD_ID) ON DELETE CASCADE)
ENGINE = INNODB;




# store URL
delimiter |

CREATE PROCEDURE PRC_STORE_URL_TTL (IN URL VARCHAR(255), IN TTL VARCHAR(100), OUT UID BIGINT UNSIGNED)
    BEGIN 
		INSERT INTO SITE (SITE_URL, SITE_TITLE)
			VALUES(URL, TTL);
        SET UID = LAST_INSERT_ID();
	END |

delimiter ;

# store WORD
delimiter |

CREATE PROCEDURE PRC_STORE_WRD (IN WORD_F VARCHAR(45), IN UID BIGINT UNSIGNED, IN EXC_AMT INT, IN EXC_PHR VARCHAR(150))
    BEGIN 
		INSERT INTO WORD (WORD_WORD)
			VALUES(WORD_F);
		INSERT INTO EXCERPT (SITE_ID, WORD_ID, EXCERPT_WRD_AMT_SITE, EXCERPT_PHRASE)
			VALUES(UID, LAST_INSERT_ID(), EXC_AMT, EXC_PHR);
	END |

delimiter ;

# return url title and excerpt of a word
delimiter |

CREATE PROCEDURE PRC_FIND_WRD (IN WORD_W VARCHAR(45))
    BEGIN 
		SELECT 	SITE_URL, SITE_TITLE, EXCERPT_PHRASE, EXCERPT_WRD_AMT_SITE
        FROM	WORD JOIN EXCERPT USING (WORD_ID) JOIN SITE USING (SITE_ID)
        WHERE	WORD_W = WORD_WORD;
	END |

delimiter ;

