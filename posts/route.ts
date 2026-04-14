import db from "@/lib/db";
import { NextResponse } from "next/server";

export async function POST(req: Request) {
    try {
        const body = await req.json();
        const {
            user_id,
            titre,
            resume,
            content,
            content_anonymise,
            topic,
            hashtags,
            language,
            status,
            completude
        } = body;

        if (!titre || !content || !user_id) {
            return NextResponse.json(
                { message: "titre, content et user_id sont requis" },
                { status: 400 }
            );
        }

        const result = await db.query(
            `INSERT INTO post 
                (user_id, titre, resume, content, content_anonymise, topic, hashtags, language, status, completude)
             VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
             RETURNING id`,
            [user_id, titre, resume, content, content_anonymise, topic, hashtags, language ?? "fr", status ?? "brouillon", completude ?? false]
        );

        return NextResponse.json(
            { message: "Post créé avec succès !", id: result.rows[0].id },
            { status: 201 }
        );

    } catch (error) {
        console.error("Post error:", error);
        return NextResponse.json(
            { message: "Erreur serveur" },
            { status: 500 }
        );
    }
}

export async function GET(req: Request) {
    try {
        const { searchParams } = new URL(req.url);
        const topic = searchParams.get("topic");
        const hashtag = searchParams.get("hashtag");

        let query = "SELECT * FROM post WHERE status = 'publie'";
        const params: string[] = [];

        if (topic) {
            params.push(topic);
            query += ` AND topic = $${params.length}`;
        }

        if (hashtag) {
            params.push(`%${hashtag}%`);
            query += ` AND hashtags LIKE $${params.length}`;
        }

        query += " ORDER BY created_at DESC";

        const result = await db.query(query, params);

        return NextResponse.json(result.rows, { status: 200 });

    } catch (error) {
        console.error("Get posts error:", error);
        return NextResponse.json(
            { message: "Erreur serveur" },
            { status: 500 }
        );
    }
}
