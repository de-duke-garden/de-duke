import markdownit from 'markdown-it';
import fs from "fs";
import path from "path";


export default function MDViewer({ content, filePath }: { content?: string, filePath?: string }) {
    const md = markdownit()
    const mdContent = content || (filePath ? fs.readFileSync(path.join(process.cwd(), filePath), "utf8") : "")
    const result = md.render(mdContent);
    return (
        <div className="mdviewer">
            <div dangerouslySetInnerHTML={{ __html: result }} />
        </div>
    );
}