package main

import (
	"database/sql"
	_ "github.com/lib/pq"
	"log"
)

type Row struct {
	x int
}

func main() {
	connStr := "postgresql://postgres:cimrubTZoW2rbU@194.169.160.225:5432?sslmode=disable"
	db, err := sql.Open("postgres", connStr)
	if err != nil {
		log.Fatal(err)
	}

	rows, err := db.Query("SELECT x FROM test")
	if err != nil {
		log.Fatal(err)
	}
	for rows.Next() {
		var x = sql.NullInt64{}

		if err := rows.Scan(&x); err != nil {
			log.Fatal(err)
		}
		value, err := x.Value()
		if err != nil {
			log.Fatal("unpacking value")
		}
		if _, ok := value.(int64); ok {
			println("x = ", value.(int64))
		} else {
			println("x = NULL")
		}
	}
}
