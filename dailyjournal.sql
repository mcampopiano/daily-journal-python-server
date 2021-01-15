CREATE TABLE `Moods` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `label` TEXT NOT NULL
);

CREATE TABLE `Notes` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `concept` TEXT NOT NULL,
    `date` TEXT NOT NULL,
    `entry` TEXT NOT NULL,
    `mood_id` INTEGER,
    FOREIGN KEY(`mood_id`) REFERENCES `Moods`(`id`)
    );

INSERT INTO moods VALUES (null, "Happy");
INSERT INTO moods VALUES (null, "Sad");
INSERT INTO moods VALUES (null, "Excited");
INSERT INTO moods VALUES (null, "Disappointed");
INSERT INTO moods VALUES (null, "Stressed");
INSERT INTO moods VALUES (null, "Accomplished");
INSERT INTO moods VALUES (null, "Pleased");
INSERT INTO moods VALUES (null, "Nervous");
INSERT INTO moods VALUES (null, "Satisfied");
INSERT INTO moods VALUES (null, "Hopeful");
INSERT INTO moods VALUES (null, "Ecstatic");

INSERT INTO notes  VALUES (null, "SQL", "01/15/21", "Learned by playing SQL Bolt", 6 );
INSERT INTO notes  VALUES (null, "PYTHON", "01/6/21", "Watched a lot of scrimba videos", 4 );

SELECT
n.concept,
n.entry,
m.label as mood
FROM Notes n
JOIN Moods m
    ON n.mood_id = m.id;