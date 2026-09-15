import { Card, CardBody } from "@heroui/react";
import { Wrench } from "lucide-react";

/** 模块占位页：真实模块开发完成后替换为对应页面组件 */
export default function ModulePlaceholder({ title }: { title: string }) {
  return (
    <div>
      <div className="mb-6">
        <h1 className="text-xl font-bold">{title}</h1>
      </div>
      <Card className="shadow-sm">
        <CardBody className="flex flex-col items-center gap-3 py-20 text-default-400">
          <Wrench size={40} />
          <p className="text-sm">「{title}」模块建设中，敬请期待</p>
          <p className="text-xs">后端接口接入后，此页面将展示实时监控与管理功能</p>
        </CardBody>
      </Card>
    </div>
  );
}
